import pytest
import uuid
from datetime import datetime, timedelta

from src.order.domain.order import Order
from src.order.domain.customer import Customer
from src.shared.domain.errors import CurrencyError, RequiredError, UUIDFormatError
from src.shared.domain.core.aggregate import Aggregate

class TestOrder:
    @pytest.fixture
    def valid_customer(self):
        return Customer.create(name="any_name", email="any_email@mail.com").value
    
    def test_order_is_an_aggregate(self):
        assert issubclass(Order, Aggregate)

    def test_create_order_with_valid_data(self, valid_customer):
        customer_id = valid_customer.id
        total = 100.50
        
        result = Order.create(
            customer_id=str(customer_id),
            total=total
        )
        
        assert result.success is True
        assert isinstance(result.value, Order)
        assert isinstance(result.value.id, uuid.UUID)
        assert str(result.value.customer_id) == str(customer_id)
        assert result.value.total == total
        assert isinstance(result.value.created_at, datetime)
        assert isinstance(result.value.updated_at, datetime)
        assert result.value.deleted_at is None
        assert result.value.is_deleted is False

    def test_create_order_with_empty_total(self, valid_customer):
        customer_id = valid_customer.id
        non_numeric_values = [
            None,
            ""
        ]
    
        for value in non_numeric_values:
            result = Order.create(customer_id=str(customer_id), total=value)
            assert result.failure is True
            assert len(result.errors) == 1
            assert result.errors[0] == RequiredError("total")
            
    def test_create_order_with_invalid_total(self, valid_customer):
        customer_id = valid_customer.id
        non_numeric_values = [
            "abc",
            [],
            {}
        ]
    
        for value in non_numeric_values:
            result = Order.create(customer_id=str(customer_id), total=value)
            assert result.failure is True
            assert len(result.errors) == 1
            assert result.errors[0] == CurrencyError("total", value)

    def test_create_order_with_negative_or_zero_total(self, valid_customer):
        customer_id = valid_customer.id
        invalid_values = [
            -100.50,
            -100,
            0
        ]
        
        for value in invalid_values:
            result = Order.create(customer_id=str(customer_id), total=value)
            assert result.failure is True
            assert len(result.errors) == 1
            assert result.errors[0] == CurrencyError("total", value)

    def test_create_order_with_empty_customer_id(self):
        result = Order.create(customer_id="", total=100.50)
        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors[0] == RequiredError("customer_id")

    def test_create_order_with_invalid_customer_id(self):
        result = Order.create(customer_id="invalid_customer_id", total=100.50)
        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors[0] == UUIDFormatError("customer_id", "invalid_customer_id")

    def test_update_order_total(self, valid_customer):
        
        order = Order.create(
            customer_id=str(valid_customer.id),
            total=100.0
        ).value
        original_updated_at = order.updated_at
        
        import time
        time.sleep(0.001)
        
        order.update_total(200.0)
        
        assert order.total == 200.0
        assert order.updated_at > original_updated_at
        assert str(order.customer_id) == str(valid_customer.id)
    
    def test_update_order_with_empty_total(self, valid_customer):
        order = Order.create(
            customer_id=str(valid_customer.id),
            total=100.0
        ).value
        non_numeric_values = [
            None,
            "",
        ]

        for value in non_numeric_values:
            result = order.update_total(value)
            assert result.failure is True
            assert len(result.errors) == 1
            assert result.errors[0] == RequiredError("total")

    def test_update_order_with_invalid_total(self, valid_customer):
        order = Order.create(
            customer_id=str(valid_customer.id),
            total=100.0
        ).value
        non_numeric_values = [
            "abc",
            [],
            {}
        ]

        for value in non_numeric_values:
            result = order.update_total(value)
            assert result.failure is True
            assert len(result.errors) == 1
            assert result.errors[0] == CurrencyError("total", value)

    def test_update_order_with_negative_or_zero_total(self, valid_customer):
        order = Order.create(
            customer_id=str(valid_customer.id),
            total=100.0
        ).value
        
        invalid_values = [
            -100.50,
            -100,
            0
        ]
        
        for value in invalid_values:
            result = order.update_total(value)
            assert result.failure is True
            assert len(result.errors) == 1
            assert result.errors[0] == CurrencyError("total", value)
            assert order.total == 100.0
    
    def test_load_existing_order(self, valid_customer):
        order_id = uuid.uuid4()
        customer_id = valid_customer.id
        total = 100.0
        created_at = datetime.now() - timedelta(days=5)
        updated_at = datetime.now() - timedelta(days=2)
        deleted_at = datetime.now() - timedelta(days=1)
        
        order = Order.load(
            id=str(order_id),
            customer_id=str(customer_id),
            total=total,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        ).value
        
        assert str(order.id) == str(order_id)
        assert str(order.customer_id) == str(customer_id)
        assert order.total == total
        assert order.created_at == created_at
        assert order.updated_at == updated_at
        assert order.deleted_at == deleted_at
        assert order.is_deleted is True

    def test_order_soft_delete(self, valid_customer):
        order = Order.create(
            customer_id=str(valid_customer.id),
            total=100.0
        ).value
        assert order.is_deleted is False
        assert order.deleted_at is None

        order.delete()
        
        assert order.is_deleted is True
        assert isinstance(order.deleted_at, datetime)
        
        assert order.total == 100.0
        assert str(order.customer_id) == str(valid_customer.id)

    def test_order_to_dict(self, valid_customer):
        order_id = uuid.uuid4()
        customer_id = valid_customer.id
        total = 150.75
        
        order = Order.load(
            id=str(order_id),
            customer_id=str(customer_id),
            total=total,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ).value
        
        result = order.to_dict()
        
        assert isinstance(result, dict)
        assert result["id"] == str(order_id)
        assert result["customer_id"] == str(customer_id)
        assert result["total"] == total
        assert "created_at" in result
        assert "updated_at" in result

    def test_create_from_dict(self, valid_customer):
        data = {
            "id": str(uuid.uuid4()),
            "customer_id": str(valid_customer.id),
            "total": 100.0,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "deleted_at": datetime.now()
        }
        
        order = Order.from_dict(data).value
        
        assert str(order.id) == str(data["id"])
        assert str(order.customer_id) == str(data["customer_id"])
        assert order.total == data["total"]
        assert order.created_at == data["created_at"]
        assert order.updated_at == data["updated_at"]
        assert order.deleted_at == data["deleted_at"]