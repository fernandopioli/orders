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
    
    def test_domain_event_creation_with_data(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        assert event.event_data == entity_for_event
        assert isinstance(event.occurred_on, datetime)
    
    def test_domain_event_creation_without_data(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        assert event.event_data == entity_for_event
        assert isinstance(event.occurred_on, datetime)
    
    def test_domain_event_creation_with_none_data(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        assert event.event_data == entity_for_event
        assert isinstance(event.occurred_on, datetime)
    
    def test_event_type_property(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        assert event.event_type == "ConcreteDomainEventImpl"
    
    def test_to_dict_serialization(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        result = event.to_dict()
        
        expected_keys = {"event_type", "occurred_on", "event_data"}
        assert set(result.keys()) == expected_keys
        assert result["event_type"] == "ConcreteDomainEventImpl"
        assert result["event_data"] == entity_for_event.to_dict()
        assert isinstance(result["occurred_on"], str)
    
    def test_to_dict_with_empty_data(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        result = event.to_dict()
        
        assert result["event_type"] == "ConcreteDomainEventImpl"
        assert result["event_data"] == entity_for_event.to_dict()
        assert isinstance(result["occurred_on"], str)
    
    def test_occurred_on_is_iso_format_in_dict(self, entity_for_event):
        event = ConcreteDomainEventImpl(entity_for_event)
        
        result = event.to_dict()
        occurred_on_str = result["occurred_on"]
        
        parsed_datetime = datetime.fromisoformat(occurred_on_str)
        assert isinstance(parsed_datetime, datetime) 