import uuid
import pytest
from unittest.mock import Mock

from src.order.domain import Order
from src.order.infrastructure.repositories import InMemoryOrderRepository


class TestInMemoryOrderRepository:
    
    @pytest.fixture
    def repository(self) -> InMemoryOrderRepository:
        return InMemoryOrderRepository()
    
    @pytest.fixture
    def valid_order(self) -> Order:
        customer_id = str(uuid.uuid4())
        result = Order.create(customer_id=customer_id, total=100.0)
        return result.value
    
    def test_save_order_successfully(self, repository: InMemoryOrderRepository, valid_order: Order):
        result = repository.save(valid_order)
        
        assert result.success is True
        assert repository.count() == 1

    def test_save_order_handles_exception(self, repository: InMemoryOrderRepository, valid_order: Order):
        mock_dict = Mock()
        mock_dict.__setitem__ = Mock(side_effect=Exception("Database connection failed"))
        
        original_orders = repository._orders
        repository._orders = mock_dict
        
        try:
            result = repository.save(valid_order)
            
            assert result.success is False
            assert result.failure is True
            assert len(result.errors) == 1
            assert "Database connection failed" in str(result.errors[0])
        finally:
            repository._orders = original_orders

    def test_save_multiple_orders(self, repository: InMemoryOrderRepository):
        order1_result = Order.create(customer_id=str(uuid.uuid4()), total=100.0)
        order2_result = Order.create(customer_id=str(uuid.uuid4()), total=200.0)
        
        repository.save(order1_result.value)
        repository.save(order2_result.value)
        
        assert repository.count() == 2
        
        result1 = repository.get_by_id(order1_result.value.id)
        result2 = repository.get_by_id(order2_result.value.id)
        
        assert result1.success is True
        assert result2.success is True
        assert result1.value.total == 100.0
        assert result2.value.total == 200.0
    
    def test_save_overwrites_existing_order(self, repository: InMemoryOrderRepository, valid_order: Order):
        repository.save(valid_order)
        
        valid_order.update_total(250.0)
        repository.save(valid_order)
        
        assert repository.count() == 1
        
        result = repository.get_by_id(valid_order.id)
        assert result.success is True
        assert result.value.total == 250.0
    
    def test_get_by_id_existing_order(self, repository: InMemoryOrderRepository, valid_order: Order):
        repository.save(valid_order)
        
        result = repository.get_by_id(valid_order.id)
        
        assert result.success is True
        assert result.value is not None
        assert result.value.id == valid_order.id
        assert result.value.total == valid_order.total
        assert result.value.customer_id == valid_order.customer_id
    
    def test_get_by_id_non_existing_order(self, repository: InMemoryOrderRepository):
        non_existing_id = uuid.uuid4()
        
        result = repository.get_by_id(non_existing_id)
        
        assert result.success is True
        assert result.value is None

    def test_get_by_id_handles_exception(self, repository: InMemoryOrderRepository):
        order_id = uuid.uuid4()
        
        mock_dict = Mock()
        mock_dict.get = Mock(side_effect=Exception("Memory corruption"))
        
        original_orders = repository._orders
        repository._orders = mock_dict
        
        try:
            result = repository.get_by_id(order_id)
            
            assert result.success is False
            assert result.failure is True
            assert len(result.errors) == 1
            assert "Memory corruption" in str(result.errors[0])
        finally:
            repository._orders = original_orders
    
    def test_clear_repository(self, repository: InMemoryOrderRepository, valid_order: Order):
        repository.save(valid_order)
        assert repository.count() == 1
        
        repository.clear()
        
        assert repository.count() == 0
        result = repository.get_by_id(valid_order.id)
        assert result.success is True
        assert result.value is None
    
    def test_get_all_orders(self, repository: InMemoryOrderRepository):
        order1_result = Order.create(customer_id=str(uuid.uuid4()), total=100.0)
        order2_result = Order.create(customer_id=str(uuid.uuid4()), total=200.0)
        
        repository.save(order1_result.value)
        repository.save(order2_result.value)
        
        result = repository.get_all()
        
        assert result.success is True
        assert len(result.value) == 2
        assert all(isinstance(order, Order) for order in result.value) 

    def test_get_all_handles_exception(self, repository: InMemoryOrderRepository):
        mock_dict = Mock()
        mock_dict.values = Mock(side_effect=Exception("Iterator error"))
        
        original_orders = repository._orders
        repository._orders = mock_dict
        
        try:
            result = repository.get_all()
            
            assert result.success is False
            assert result.failure is True
            assert len(result.errors) == 1
            assert "Iterator error" in str(result.errors[0])
        finally:
            repository._orders = original_orders