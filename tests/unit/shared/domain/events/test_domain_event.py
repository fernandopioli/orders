import uuid
import pytest
from datetime import datetime
from abc import ABC

from src.shared.domain.events import DomainEvent
from src.shared.domain.core import Entity

class ConcreteDomainEventImpl(DomainEvent):
    def __init__(self, entity: Entity):
        super().__init__(entity)
    
    def __repr__(self) -> str:
        return f"ConcreteDomainEventImpl(event_data={self.event_data.id})"

class ConcreteEntityForEvent(Entity):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return super().to_dict()
    
    def validate(self):
        pass

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=uuid.UUID(data["id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            deleted_at=datetime.fromisoformat(data["deleted_at"]),
        )

class TestDomainEvent:

    @pytest.fixture
    def entity_for_event(self):
        return ConcreteEntityForEvent()
    
    def test_domain_event_is_abstract(self):
        assert issubclass(DomainEvent, ABC)
        
        with pytest.raises(TypeError):
            DomainEvent()
    
    def test_domain_event_creation(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        assert isinstance(uuid.UUID(event.event_id), uuid.UUID)
        assert event.event_type == "ConcreteDomainEventImpl"
        assert event.aggregate_id == entity_for_event.id
        assert event.event_data == entity_for_event
        assert isinstance(event.occurred_on, datetime)
        assert event.version == 1
    
    def test_to_dict_serialization(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        result = event.to_dict()
        
        expected_keys = {"event_type", "occurred_on", "event_data", "aggregate_id", "event_id", "version"}
        assert set(result.keys()) == expected_keys
        assert result["event_id"] == event.event_id
        assert result["aggregate_id"] == str(entity_for_event.id)
        assert result["event_type"] == "ConcreteDomainEventImpl"
        assert result["event_data"] == entity_for_event.to_dict()
        assert isinstance(result["occurred_on"], str)
        assert result["version"] == 1
    
    def test_occurred_on_is_iso_format_in_dict(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        result = event.to_dict()
        occurred_on_str = result["occurred_on"]
        
        parsed_datetime = datetime.fromisoformat(occurred_on_str)
        assert isinstance(parsed_datetime, datetime) 