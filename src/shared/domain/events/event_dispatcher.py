from typing import Dict, List

from src.shared.domain.core import Result
from src.shared.domain.core.entity import Entity
from src.shared.domain.events.domain_event import DomainEvent
from src.shared.domain.events.event_publisher import EventPublisher


class EventDispatcher:
    
    def __init__(self, publisher: EventPublisher, topic_mapping: Dict[str, str] | None = None):
        self.publisher = publisher
        self.topic_mapping = topic_mapping or self._default_topic_mapping()
    
    def dispatch_from_entity(self, entity: Entity) -> Result[None]:
        events = entity.get_events()
        
        if not events:
            return Result.ok()
        
        for event in events:
            result = self._dispatch_single_event(event)
            if result.failure:
                return result
        
        entity.clear_events()
        return Result.ok()
    
    def dispatch_events(self, events: List[DomainEvent]) -> Result[None]:
        for event in events:
            result = self._dispatch_single_event(event)
            if result.failure:
                return result
        
        return Result.ok()
    
    def _dispatch_single_event(self, event: DomainEvent) -> Result[None]:
        topic = self._get_topic_for_event(event)
        
        if not topic:
            return Result.fail([f"Topic not found for event: {event.event_type}"])
        
        return self.publisher.publish(event, topic)
    
    def _get_topic_for_event(self, event: DomainEvent) -> str | None:
        return self.topic_mapping.get(event.event_type)
    
    def add_topic_mapping(self, event_type: str, topic: str) -> None:
        self.topic_mapping[event_type] = topic
    
    def _default_topic_mapping(self) -> Dict[str, str]:
        return {
            "OrderCreatedEvent": "order-events"
        } 