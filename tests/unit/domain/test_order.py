import pytest
import uuid
from datetime import datetime, timedelta

from src.domain.order import Order
from src.domain.entity import Entity
from src.domain.customer import Customer

class TestOrder:
    @pytest.fixture
    def valid_customer(self):
        return Customer.create(name="any_name", email="any_email@mail.com")

    def test_create_order_with_valid_data(self, valid_customer):
        customer_id = valid_customer.id
        total = 100.50
        
        order = Order.create(
            customer_id=customer_id,
            total=total
        )
        
        assert isinstance(order, Entity)
        assert isinstance(order.id, uuid.UUID)
        assert order.customer_id == customer_id
        assert order.total == total
        assert isinstance(order.created_at, datetime)
        assert isinstance(order.updated_at, datetime)
        assert order.deleted_at is None
        assert order.is_deleted is False

    def test_create_order_with_invalid_total(self, valid_customer):
        customer_id = valid_customer.id
        non_numeric_values = [
            "abc",
            None,
            "",
            [],
            {}
        ]
    
        for value in non_numeric_values:
            with pytest.raises(TypeError) as excinfo:
                Order.create(customer_id=customer_id, total=value)
            assert "Order total must be a number" in str(excinfo.value)

    def test_create_order_with_negative_or_zero_total(self, valid_customer):
        customer_id = valid_customer.id
        invalid_values = [
            -100.50,
            -100,
            0
        ]
        
        for value in invalid_values:
            with pytest.raises(ValueError) as excinfo:
                Order.create(customer_id=customer_id, total=value)
            assert "Order total must be greater than zero" in str(excinfo.value)

    def test_create_order_with_invalid_customer_id(self):
        with pytest.raises(TypeError) as excinfo:
            Order.create(customer_id="invalid_customer_id", total=100.50)
        assert "Customer ID must be a valid UUID" in str(excinfo.value)

    def test_update_order_total(self, valid_customer):
        
        order = Order.create(
            customer_id=valid_customer.id,
            total=100.0
        )
        original_updated_at = order.updated_at
        
        import time
        time.sleep(0.001)
        
        order.update_total(200.0)
        
        assert order.total == 200.0
        assert order.updated_at > original_updated_at
        assert order.customer_id == valid_customer.id
    
    def test_update_order_with_invalid_total(self, valid_customer):
        order = Order.create(
            customer_id=valid_customer.id,
            total=100.0
        )
        non_numeric_values = [
            "abc",
            None,
            "",
            [],
            {}
        ]

        for value in non_numeric_values:
            with pytest.raises(TypeError) as excinfo:
                order.update_total(value)
            assert "Order total must be a number" in str(excinfo.value)

    def test_update_order_with_negative_or_zero_total(self, valid_customer):
        order = Order.create(
            customer_id=valid_customer.id,
            total=100.0
        )
        
        invalid_values = [
            -100.50,
            -100,
            0
        ]
        
        for value in invalid_values:
            with pytest.raises(ValueError) as excinfo:
                order.update_total(value)
            assert "Order total must be greater than zero" in str(excinfo.value)
            assert order.total == 100.0
    
    def test_load_existing_order(self, valid_customer):
        order_id = uuid.uuid4()
        customer_id = valid_customer.id
        total = 100.0
        created_at = datetime.now() - timedelta(days=5)
        updated_at = datetime.now() - timedelta(days=2)
        deleted_at = datetime.now() - timedelta(days=1)
        
        order = Order.load(
            id=order_id,
            customer_id=customer_id,
            total=total,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )
        
        assert order.id == order_id
        assert order.customer_id == customer_id
        assert order.total == total
        assert order.created_at == created_at
        assert order.updated_at == updated_at
        assert order.deleted_at == deleted_at
        assert order.is_deleted is True

    def test_order_soft_delete(self, valid_customer):
        order = Order.create(
            customer_id=valid_customer.id,
            total=100.0
        )
        assert order.is_deleted is False
        assert order.deleted_at is None

        order.delete()
        
        assert order.is_deleted is True
        assert isinstance(order.deleted_at, datetime)
        
        assert order.total == 100.0
        assert order.customer_id == valid_customer.id

    def test_order_to_dict(self, valid_customer):
        order_id = uuid.uuid4()
        customer_id = valid_customer.id
        total = 150.75
        
        order = Order(
            id=order_id,
            customer_id=customer_id,
            total=total
        )
        
        result = order.to_dict()
        
        assert isinstance(result, dict)
        assert result["id"] == str(order_id)
        assert result["customer_id"] == str(customer_id)
        assert result["total"] == total
        assert "created_at" in result
        assert "updated_at" in result

    def test_create_from_dict(self, valid_customer):
        data = {
            "customer_id": str(valid_customer.id),
            "total": 100.0
        }
        
        order = Order.from_dict(data)
        
        # assert isinstance(order, Order)
        # assert order.customer_id == valid_customer.id
        # assert order.total == 100.0
        # assert isinstance(order.id, uuid.UUID)
        # assert isinstance(order.created_at, datetime)
        # assert isinstance(order.updated_at, datetime)
        # assert order.deleted_at is None
        # assert order.is_deleted is False