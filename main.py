import argparse
import asyncio
import logging
import sys
import os
import sys
import sbsip

from datetime import datetime, date
from pathlib import Path
from datafordeler import Datafordeler
from odk_tools.reporting import report
from process.mssql_client import MSSQLClient

from automation_server_client import (
    AutomationServer,
    Workqueue,
    WorkItemError,
    Credential,
    WorkItemStatus,
)

mssql_client: MSSQLClient
proces_navn = "Brevafsendelse BMF Bosætningsstrategi"
fordeler: Datafordeler
OVERSKRIFT = "Velkommen til Odense"
BESKRIVELSE = "Velkommen til Odense - Bosætningsstrategi"
SBSYS_SKABELON_ID = ""
sag_på_brev = False

async def populate_queue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    logger.info("Hello from populate workqueue!")

    borgere = mssql_client.hent_borgere()
    
    for borger in borgere:
        cpr = borger["Cpr"]
        personoplysninger = fordeler.hent_personoplysninger(cpr)
        cpr_fordeler = personoplysninger["Person"]["Personnumre"][0]["Personnummer"]["personnummer"]
        try:
            if not cpr_fordeler == cpr:
                logger.warning(f"cpr stemmer ikke overens: {borger}")
                continue
        except KeyError:
            logger.warning(f"Missing Cpr for borger: {borger}")
            continue

        data = {
            "cpr": cpr
        }

        # tjek om item allerede er i kø inden det bliver sendt ned til process
        if not workqueue.get_item_by_reference(cpr, status=WorkItemStatus.IN_PROGRESS):
            workqueue.add_item(data=data, reference=str(cpr))


async def process_workqueue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    logger.info("Hello from process workqueue!")

    for item in workqueue:
        with item:
            data = item.data  # Item data deserialized from json as dict
            cpr = data["cpr"]
 
            try:
                #TODO: 
                borger_adresse, borger_post_nr = fordeler.hent_adresse_til_sbsip(cpr)
                
                try:
                    
                    # Send the existing PDF directly; no Word merge/render step is needed.
                    sbsip.send_digital_post(
                        vedhæftet_fil=Path(args.file_template),
                        cpr=cpr,
                        post_nr=borger_post_nr,
                        adresse=borger_adresse,
                        overskrift="Annes testbrev",
                        beskrivelse="bmf bosætningsstragtegi testbrev",
                        sbsys_skabelon_id=""
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

    certifikat_sti = os.getenv("CERTIFICATES", "certificates")
    fordeler = Datafordeler(
        certifikat_sti=os.path.join(certifikat_sti, "datafordeler.crt"),
        certifikat_nøglefil=os.path.join(certifikat_sti, "datafordeler.key"),
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
