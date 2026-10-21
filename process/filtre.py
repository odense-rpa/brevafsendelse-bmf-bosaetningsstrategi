"""Tjek der afgør, om en borger skal springes over ved udfyldning af køen."""

from datetime import UTC, datetime, timedelta

from automation_server_client import WorkItem
from datafordeler.modeller import Person


def bor_i_odense(person: Person) -> bool:
    """Borgeren er i live og har en aktuel adresse i Odense Kommune."""
    return (
        not person.er_død
        and person.adresse is not None
        and person.adresse.bor_i_kommune()
    )


def er_kørt_for_nylig(items: list[WorkItem], dage: int) -> bool:
    """Et af itemsene (uanset status) er oprettet inden for de seneste `dage` dage.

    ATS-tidspunkter uden tidszone antages at være UTC.
    """
    graense = datetime.now(UTC) - timedelta(days=dage)
    return any(
        (
            item.created_at
            if item.created_at.tzinfo
            else item.created_at.replace(tzinfo=UTC)
        )
        >= graense
        for item in items
    )
