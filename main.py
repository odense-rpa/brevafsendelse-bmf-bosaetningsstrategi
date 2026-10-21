import argparse
import asyncio
import logging
import os
import sys
import sbsip
from datetime import UTC, datetime, timedelta

from automation_server_client import (
    AutomationServer,
    Credential,
    WorkItemError,
    WorkItemStatus,
    Workqueue,
)

from pathlib import Path
from datafordeler import DatafordelerGraphQL
from odk_tools.reporting import report
from process.mssql_client import MSSQLClient


proces_navn = "Brevafsendelse BMF Bosætningsstrategi"
DAGE_MELLEM_BREVE = 35
mssql_client: MSSQLClient
fordeler: DatafordelerGraphQL


def _som_utc(tidspunkt: datetime) -> datetime:
    """Gør tidspunkter uden tidszone sammenlignelige (ATS-tidspunkter antages at være UTC)."""
    return tidspunkt if tidspunkt.tzinfo else tidspunkt.replace(tzinfo=UTC)


async def populate_queue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    logger.info("Hello from populate workqueue!")

    borgere = mssql_client.hent_borgere()


    for borger in borgere:
        cpr = str(borger["Cpr"]).replace("-", "")
        # TODO: Med REST-klienten blev det første personnummer fra Datafordeleren
        # sammenlignet med cpr, og borgeren blev sprunget over ved forskel. Datafordeler
        # 1.0.0 returnerer ikke personnumre, så tjekket er nu kun, at personen findes
        # (hent_person giver ValueError ellers). Afklar om borgere med ændret CPR skal
        # springes over, og om ValueError skal fanges i stedet for at stoppe hele køen.
        fordeler.hent_person(cpr)

        data = {"cpr": cpr}

        # spring borgere over, som allerede har et item i ATS inden for de seneste 35 dage
        graense = datetime.now(UTC) - timedelta(days=DAGE_MELLEM_BREVE)
        tidligere_items = workqueue.get_item_by_reference(cpr)
        if any(_som_utc(item.created_at) >= graense for item in tidligere_items):
            logger.info("Borger har allerede været kørt inden for %s dage", DAGE_MELLEM_BREVE)
            continue

        workqueue.add_item(data=data, reference=cpr)


async def process_workqueue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    logger.info("Hello from process workqueue!")

    for item in workqueue:
        with item:
            data = item.data  # Item data deserialized from json as dict
            cpr = data["cpr"]

            try:
                # TODO:
                borger_adresse, borger_post_nr = fordeler.hent_person(cpr).sbsip_adresse()

                try:
                    # Send the existing PDF directly; no Word merge/render step is needed.
                    sbsip.send_digital_post(
                        vedhæftet_fil=Path(args.file_template),
                        cpr=cpr,
                        post_nr=borger_post_nr,
                        adresse=borger_adresse,
                        overskrift="Annes testbrev",
                        beskrivelse="bmf bosætningsstragtegi testbrev",
                    )
                except Exception as error:
                    logger.exception("Brevafsendelse fejlede")
                    raise WorkItemError(f"Brev kunne ikke sendes: {error}") from error

                report("sbsys-brevsender", "Brev sendt", {"CPR": cpr})

            except WorkItemError as e:
                # A WorkItemError represents a soft error that indicates the item should be passed to manual processing or a business logic fault
                report("sbsys-brevsender", "Brev blev ikke sendt", {"CPR": cpr})

                logger.error(f"Error processing item: {data}. Error: {e}")
                item.fail(str(e))


if __name__ == "__main__":
    ats = AutomationServer.from_environment()
    workqueue = ats.workqueue()

    # Initialize external systems for automation here..
    sbsip_credential = Credential.get_credential("SBSip - produktion")

    parser = argparse.ArgumentParser(description=proces_navn)

    tracking_credential = Credential.get_credential("Odense SQL Server")
    datafordeler_credential = Credential.get_credential("Datafordeler")

    mssql_client = MSSQLClient(
        host=tracking_credential.data["server"],  # Assuming username contains host
        user=tracking_credential.username,
        password=tracking_credential.password,
        database=tracking_credential.data["database"],
    )

    parser.add_argument(
        "--queue",
        action="store_true",
        help="Udfyld køen og afslut",
    )

    parser.add_argument(
        "--file-template",
        default=os.environ.get("FILE_TEMPLATE_PATH"),
        help="Path to the file template for letter generation",
    )

    fordeler = DatafordelerGraphQL(
        client_id=datafordeler_credential.username,
        client_secret=datafordeler_credential.password,
    )

    args = parser.parse_args()
    sbsip.start_sbsip(
        brugernavn=sbsip_credential.username,
        adgangskode=sbsip_credential.password,
    )

    # Queue management
    if "--queue" in sys.argv:
        workqueue.clear_workqueue(WorkItemStatus.NEW)
        asyncio.run(populate_queue(workqueue))
        exit(0)

    # Process workqueue
    asyncio.run(process_workqueue(workqueue))
