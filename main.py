import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

import sbsip
from automation_server_client import (
    AutomationServer,
    Credential,
    WorkItemStatus,
    Workqueue,
)
from datafordeler import DatafordelerGraphQL
from odk_tools.reporting import report

from process.config import (
    BREV_BESKRIVELSE,
    BREV_OVERSKRIFT,
    CREDENTIAL_DATAFORDELER,
    CREDENTIAL_SBSIP,
    CREDENTIAL_SQL,
    DAGE_MELLEM_BREVE,
    PROCES_NAVN,
    RAPPORT_ARK_ANTAL,
    RAPPORT_ARK_FEJL,
    RAPPORT_NAVN,
)
from process.filtre import bor_i_odense, er_kørt_for_nylig
from process.mssql_client import MSSQLClient

mssql_client: MSSQLClient
fordeler: DatafordelerGraphQL


async def populate_queue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    logger.info("Hello from populate workqueue!")

    borgere = mssql_client.hent_borgere()

    for borger in borgere:
        cpr = str(borger["Cpr"]).replace("-", "")
        # TODO: Med REST-klienten blev det første personnummer fra Datafordeleren
        # sammenlignet med cpr, og borgeren blev sprunget over ved forskel. Datafordeler
        # 1.0.0 returnerer ikke personnumre, så tjekket er nu kun, at personen findes
        # (hent_person giver ValueError ellers). Bopælstjekket nedenfor springer borgere over,
        # som ikke bor i Odense Kommune. Afklar om borgere med ændret CPR skal
        # springes over, og om ValueError skal fanges i stedet for at stoppe hele køen.
        person = fordeler.hent_person(cpr)

        if not bor_i_odense(person):
            logger.info("Borger bor ikke længere i Odense Kommune, springes over")
            continue

        if er_kørt_for_nylig(workqueue.get_item_by_reference(cpr), DAGE_MELLEM_BREVE):
            logger.info(
                "Borger har allerede været kørt inden for %s dage", DAGE_MELLEM_BREVE
            )
            continue

        workqueue.add_item(data={"cpr": cpr}, reference=cpr)


async def process_workqueue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    logger.info("Hello from process workqueue!")

    antal_sendt = 0

    for item in workqueue:
        with item:
            data = item.data  # Item data deserialized from json as dict
            cpr = data["cpr"]

            try:
                borger_adresse, borger_post_nr = fordeler.hent_person(
                    cpr
                ).sbsip_adresse()

                # Send the existing PDF directly; no Word merge/render step is needed.
                sbsip.send_digital_post(
                    vedhæftet_fil=Path(args.file_template),
                    cpr=cpr,
                    post_nr=borger_post_nr,
                    adresse=borger_adresse,
                    overskrift=BREV_OVERSKRIFT,
                    beskrivelse=BREV_BESKRIVELSE,
                )
                antal_sendt += 1

            except Exception as error:
                # Uanset årsag: marker itemet som fejlet, rapportér og fortsæt med næste borger
                logger.exception("Brev kunne ikke sendes")
                report(
                    RAPPORT_NAVN, RAPPORT_ARK_FEJL, {"CPR": cpr, "Årsag": str(error)}
                )
                item.fail(str(error))

    # Kun antallet rapporteres: ingen oplysninger om hvem, hvad eller hvornår
    report(RAPPORT_NAVN, RAPPORT_ARK_ANTAL, {"Antal breve sendt": antal_sendt})


if __name__ == "__main__":
    ats = AutomationServer.from_environment()
    workqueue = ats.workqueue()

    # Initialize external systems for automation here..
    sbsip_credential = Credential.get_credential(CREDENTIAL_SBSIP)

    parser = argparse.ArgumentParser(description=PROCES_NAVN)

    tracking_credential = Credential.get_credential(CREDENTIAL_SQL)
    datafordeler_credential = Credential.get_credential(CREDENTIAL_DATAFORDELER)

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
        help="Sti til brevets PDF (fx på shared drive). Standard er FILE_TEMPLATE_PATH",
    )

    fordeler = DatafordelerGraphQL(
        client_id=datafordeler_credential.username,
        client_secret=datafordeler_credential.password,
    )

    args = parser.parse_args()
    if "--queue" not in sys.argv and not (
        args.file_template and Path(args.file_template).is_file()
    ):
        raise FileNotFoundError(
            f"Brevets PDF ikke fundet: {args.file_template!r} (angiv --file-template eller FILE_TEMPLATE_PATH)"
        )
    sbsip.start_sbsip(
        brugernavn=sbsip_credential.username,
        adgangskode=sbsip_credential.password,
    )

    # Queue management
    if "--queue" in sys.argv:
        workqueue.clear_workqueue(WorkItemStatus.NEW)
        asyncio.run(populate_queue(workqueue))
        sys.exit(0)

    # Process workqueue
    asyncio.run(process_workqueue(workqueue))
