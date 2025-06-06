from typing import TYPE_CHECKING
from src.shared.domain.events.domain_event import DomainEvent

if TYPE_CHECKING:
    from src.order.domain.order import Order


class OrderCreatedEvent(DomainEvent):
    def __init__(self, order: "Order"):
        super().__init__(order)
    
    def __repr__(self) -> str:
        return f"OrderCreatedEvent(id={self.event_data.id})"