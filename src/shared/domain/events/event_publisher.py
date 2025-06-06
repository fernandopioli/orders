from abc import ABC, abstractmethod

from src.shared.domain.core import Result
from src.shared.domain.events.domain_event import DomainEvent


class EventPublisher(ABC):
    
    @abstractmethod
    def publish(self, event: DomainEvent, topic: str) -> Result[None]:
        pass