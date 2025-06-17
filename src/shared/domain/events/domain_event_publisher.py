from typing import Dict, List

from src.shared.domain.events import DomainEvent, DomainEventHandler


class DomainEventPublisher:
    def __init__(self):
        self._handlers: Dict[str, List[DomainEventHandler]] = {}

    def subscribe(self, event_type: str, handler: DomainEventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        handler_type = type(handler).__name__
        existing_handler_types = [type(h).__name__ for h in self._handlers[event_type]]

        if handler_type not in existing_handler_types:
            self._handlers[event_type].append(handler)

    def publish(self, events: List[DomainEvent]) -> None:
        for event in events:
            event_type = type(event).__name__
            handlers = self._handlers.get(event_type, [])
            for handler in handlers:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"Error handling event {event.event_type}: {e}")
