import argparse
import asyncio
import logging
import sys
import os
import sys
from odk_tools.tracking import Tracker
import sbsip
import sbsys_brevsender

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

async def populate_queue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    logger.info("Hello from populate workqueue!")

    #TODO: hent personer i databasen der skal bearbejdes
    borgere = mssql_client.hent_borgere()
    print("hej")
    #cpr = fordeler.hent_personoplysninger("cpr")

    #TODO: check om item allerede eksisterer i køen

    data = {
        "cpr": cpr
    }


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
                    # send brev - husk at tjek, om du skal lave sag eller ej
                    sbsys_brevsender.flet_og_send_brev(
                        fil_sti=args.word_template,
                        brev_felter=data["borger_data"],
                        cpr=cpr,
                        post_nr=borger_post_nr,
                        adresse=borger_adresse,
                        overskrift=OVERSKRIFT,
                        beskrivelse=BESKRIVELSE,
                        sbsys_skabelon_id=SBSYS_SKABELON_ID if sag_på_brev else ""
                    )
                except:
                    raise WorkItemError(f"Brev kunne ikke sendes")


                report("sbsys-brevsender", "Brev sendt", {"CPR": cpr})

            except WorkItemError as e:
                # A WorkItemError represents a soft error that indicates the item should be passed to manual processing or a business logic fault
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
        "--word-template",
        default=os.environ.get("WORD_TEMPLATE_PATH"),
        help="Path to the Word template for letter generation",
    )
    args = parser.parse_args()

    certifikat_sti = os.getenv("CERTIFICATES", "certificates")
    fordeler = Datafordeler(
        certifikat_sti=os.path.join(certifikat_sti, "datafordeler.crt"),
        certifikat_nøglefil=os.path.join(certifikat_sti, "datafordeler.key"),
    )
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
