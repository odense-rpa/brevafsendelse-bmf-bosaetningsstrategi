"""Tjek der afgør, om en borger skal springes over ved udfyldning af køen."""

from datetime import UTC, datetime, timedelta

from automation_server_client import WorkItem, WorkItemStatus
from datafordeler.modeller import Person


def bor_i_odense(person: Person) -> bool:
    """Borgeren er i live og har en aktuel adresse i Odense Kommune."""
    return (
        not person.er_død
        and person.adresse is not None
        and person.adresse.bor_i_kommune()
    )


def er_kørt_for_nylig(items: list[WorkItem], dage: int) -> bool:
    """Et af de færdige items er oprettet inden for de seneste `dage` dage.

    Fejlede items tæller ikke med, så borgeren kan få et nyt forsøg.
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
        if item.status == WorkItemStatus.COMPLETED
    )
