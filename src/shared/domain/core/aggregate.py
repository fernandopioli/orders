import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from src.shared.domain.core.entity import Entity

if TYPE_CHECKING:
    from src.shared.domain.events import DomainEvent


class Aggregate(Entity):
    def __init__(
        self,
        id: uuid.UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        deleted_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at, deleted_at)
        self._domain_events: List["DomainEvent"] = []

    def add_domain_event(self, event: "DomainEvent") -> None:
        self._domain_events.append(event)

    def get_events(self) -> List["DomainEvent"]:
        return self._domain_events

    def clear_events(self) -> None:
        self._domain_events = []
