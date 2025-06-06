import pytest
import uuid
from datetime import datetime
from abc import ABC

from src.order.domain.order import Order
from src.order.domain.order_created_event import OrderCreatedEvent
from src.shared.domain.events.domain_event import DomainEvent


class TestOrderCreatedEvent:
    
    @pytest.fixture
    def sample_order(self):
        customer_id = str(uuid.uuid4())
        return Order.create(customer_id, 299.99).value
    
    def test_order_created_event_inherits_from_domain_event(self):
        assert issubclass(OrderCreatedEvent, DomainEvent)
    
    def test_order_created_event_creation_with_order(self, sample_order):
        event = OrderCreatedEvent(sample_order)
        
        assert isinstance(event, OrderCreatedEvent)
        assert isinstance(event.occurred_on, datetime)
        assert isinstance(event.event_data, Order)
    
    def test_event_type_property(self, sample_order):
        event = OrderCreatedEvent(sample_order)
        
        assert event.event_type == "OrderCreatedEvent"
    
    def test_event_data_contains_order_information(self, sample_order):
        event = OrderCreatedEvent(sample_order)
        
        assert event.event_data == sample_order
    
    def test_repr_method(self, sample_order):
        event = OrderCreatedEvent(sample_order)
        repr_str = repr(event)
        
        assert "OrderCreatedEvent" in repr_str
        assert "id=" in repr_str
        assert str(sample_order.id) in repr_str
        
        expected_repr = f"OrderCreatedEvent(id={sample_order.id})"
        assert repr_str == expected_repr
