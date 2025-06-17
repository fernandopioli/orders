import uuid
from datetime import datetime

import pytest

from src.shared.domain.core import Aggregate, Entity
from src.shared.domain.events import DomainEvent


class ConcreteAggregate(Aggregate):
    def __repr__(self) -> str:
        return f"ConcreteAggregate(id={self.id})"

    def validate(self) -> None:
        pass

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict) -> "ConcreteAggregate":
        return cls(
            id=uuid.UUID(data["id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            deleted_at=datetime.fromisoformat(data["deleted_at"]),
        )


class ConcreteEventForTesting(DomainEvent):
    def __init__(self, aggregate: Aggregate):
        super().__init__(aggregate)

    def __repr__(self) -> str:
        return f"ConcreteEventForTesting(aggregate_id={self.event_data.id})"


class TestAggregate:
    @pytest.fixture
    def concrete_aggregate(self):
        return ConcreteAggregate()

    @pytest.fixture
    def concrete_event(self, concrete_aggregate):
        return ConcreteEventForTesting(concrete_aggregate)

    def test_aggregate_is_abstract(self):
        with pytest.raises(TypeError):
            Aggregate()

    def test_aggregate_is_an_entity(self):
        assert issubclass(Aggregate, Entity)

    def test_aggregate_creation_with_no_parameters(self):
        aggregate = ConcreteAggregate()

        assert isinstance(aggregate.id, uuid.UUID)
        assert isinstance(aggregate.created_at, datetime)
        assert isinstance(aggregate.updated_at, datetime)
        assert aggregate.deleted_at is None

    def test_aggregate_creation_with_parameters(self):
        id = uuid.uuid4()
        created_at = datetime.now()
        updated_at = datetime.now()
        deleted_at = datetime.now()

        aggregate = ConcreteAggregate(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
        )

        assert aggregate.id == id
        assert aggregate.created_at == created_at
        assert aggregate.updated_at == updated_at
        assert aggregate.deleted_at == deleted_at

    def test_aggregate_starts_with_empty_events_list(self, concrete_aggregate):
        events = concrete_aggregate.get_events()

        assert isinstance(events, list)
        assert len(events) == 0

    def test_add_domain_event_single_event(self, concrete_aggregate, concrete_event):
        concrete_aggregate.add_domain_event(concrete_event)
        events = concrete_aggregate.get_events()

        assert len(events) == 1
        assert events[0] == concrete_event
        assert events[0].event_data.id == concrete_aggregate.id

    def test_add_domain_event_multiple_events(self, concrete_aggregate):
        event1 = ConcreteEventForTesting(concrete_aggregate)
        event2 = ConcreteEventForTesting(concrete_aggregate)
        event3 = ConcreteEventForTesting(concrete_aggregate)

        concrete_aggregate.add_domain_event(event1)
        concrete_aggregate.add_domain_event(event2)
        concrete_aggregate.add_domain_event(event3)

        events = concrete_aggregate.get_events()

        assert len(events) == 3
        assert events[0] == event1
        assert events[1] == event2
        assert events[2] == event3

    def test_get_events_returns_list(self, concrete_aggregate, concrete_event):
        concrete_aggregate.add_domain_event(concrete_event)

        events1 = concrete_aggregate.get_events()
        events2 = concrete_aggregate.get_events()

        assert events1 == events2
        assert len(events1) == 1
        assert len(events2) == 1
        assert events1[0] == concrete_event
        assert events2[0] == concrete_event

    def test_clear__all_events(self, concrete_aggregate):
        event1 = ConcreteEventForTesting(concrete_aggregate)
        event2 = ConcreteEventForTesting(concrete_aggregate)

        concrete_aggregate.add_domain_event(event1)
        concrete_aggregate.add_domain_event(event2)

        assert len(concrete_aggregate.get_events()) == 2

        concrete_aggregate.clear_events()

        events = concrete_aggregate.get_events()
        assert len(events) == 0

    def test_clear_events_on_empty_list(self, concrete_aggregate):
        assert len(concrete_aggregate.get_events()) == 0

        concrete_aggregate.clear_events()

        assert len(concrete_aggregate.get_events()) == 0
