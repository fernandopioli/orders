from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.shared.domain.events import DomainEvent

class DomainEventHandler(ABC):
    @abstractmethod
    def handle(self, event: "DomainEvent") -> None:
        pass