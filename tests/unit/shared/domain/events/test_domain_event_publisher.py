from contextlib import nullcontext as does_not_raise
from unittest.mock import Mock

from src.shared.domain.events import (
    DomainEvent,
    DomainEventHandler,
    DomainEventPublisher,
)


class MockEmailHandler(DomainEventHandler):
    def handle(self, event: DomainEvent) -> None:
        print(f"Email sent for event: {event.event_type}")


class MockSmsHandler(DomainEventHandler):
    def handle(self, event: DomainEvent) -> None:
        print(f"SMS sent for event: {event.event_type}")


class UserCreatedEvent(DomainEvent):
    def __init__(self, user: any):
        self.user = user

    def __repr__(self) -> str:
        return f"UserCreatedEvent(user={self.user})"


class UserUpdatedEvent(DomainEvent):
    def __init__(self, user: any):
        self.user = user

    def __repr__(self) -> str:
        return f"UserUpdatedEvent(user={self.user})"


class TestDomainEventPublisher:
    def test_domain_event_publisher_creation_with_no_handlers(self):
        publisher = DomainEventPublisher()

        assert publisher._handlers == {}

    def test_domain_event_publisher_subscribe_to_event(self):
        publisher = DomainEventPublisher()
        publisher.subscribe("UserCreatedEvent", MockEmailHandler())

        assert "UserCreatedEvent" in publisher._handlers
        assert len(publisher._handlers["UserCreatedEvent"]) == 1

    def test_domain_event_publisher_subscribe_multiple_different_handlers(self):
        publisher = DomainEventPublisher()
        email_handler = MockEmailHandler()
        sms_handler = MockSmsHandler()

        publisher.subscribe("UserCreatedEvent", email_handler)
        publisher.subscribe("UserCreatedEvent", sms_handler)

        assert "UserCreatedEvent" in publisher._handlers
        assert len(publisher._handlers["UserCreatedEvent"]) == 2

        handler_types = [type(h).__name__ for h in publisher._handlers["UserCreatedEvent"]]
        assert "MockEmailHandler" in handler_types
        assert "MockSmsHandler" in handler_types

    def test_domain_event_publisher_prevents_duplicate_handler_types(self):
        publisher = DomainEventPublisher()
        handler1 = MockEmailHandler()
        handler2 = MockEmailHandler()

        publisher.subscribe("UserCreatedEvent", handler1)
        publisher.subscribe("UserCreatedEvent", handler2)

        assert "UserCreatedEvent" in publisher._handlers
        assert len(publisher._handlers["UserCreatedEvent"]) == 1

        assert type(publisher._handlers["UserCreatedEvent"][0]).__name__ == "MockEmailHandler"

    def test_domain_event_publisher_multiple_events(self):
        publisher = DomainEventPublisher()
        handler1 = MockEmailHandler()
        handler2 = MockSmsHandler()

        publisher.subscribe("UserCreatedEvent", handler1)
        publisher.subscribe("UserUpdatedEvent", handler2)

        assert "UserUpdatedEvent" in publisher._handlers
        assert len(publisher._handlers["UserUpdatedEvent"]) == 1

        assert type(publisher._handlers["UserUpdatedEvent"][0]).__name__ == "MockSmsHandler"

        assert "UserCreatedEvent" in publisher._handlers
        assert len(publisher._handlers["UserCreatedEvent"]) == 1

        assert type(publisher._handlers["UserCreatedEvent"][0]).__name__ == "MockEmailHandler"

    def test_domain_event_publisher_handlers_are_called(self):
        publisher = DomainEventPublisher()
        mock_handler = Mock(spec=MockEmailHandler)

        event = UserCreatedEvent(user="id")

        publisher.subscribe("UserCreatedEvent", mock_handler)
        publisher.publish([event])

        mock_handler.handle.assert_called_once_with(event)

    def test_domain_event_publisher_handler_not_raise_exception(self):
        publisher = DomainEventPublisher()
        mock_handler = Mock(spec=MockEmailHandler)

        event = UserCreatedEvent(user="id")

        publisher.subscribe("UserCreatedEvent", mock_handler)
        mock_handler.handle.side_effect = Exception("Test exception")

        with does_not_raise():
            publisher.publish([event])
