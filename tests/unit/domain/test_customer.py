import uuid
from datetime import datetime, timedelta

import pytest

from src.domain.customer import Customer
from src.domain.entity import Entity


class TestCustomer:

    def test_create_customer_with_valid_data(self):
        name = "Any name"
        email = "any_email@mail.com"

        customer = Customer.create(name=name, email=email)

        assert isinstance(customer, Entity)
        assert isinstance(customer.id, uuid.UUID)
        assert customer.name == name
        assert customer.email == email
        assert isinstance(customer.created_at, datetime)
        assert isinstance(customer.updated_at, datetime)
        assert customer.deleted_at is None
        assert customer.is_deleted is False

    def test_customer_with_empty_name(self):
        empty_name = ""
        email = "any_email@mail.com"

        with pytest.raises(ValueError) as excinfo:
            Customer.create(name=empty_name, email=email)

        assert "Name cannot be empty" in str(excinfo.value)

    def test_customer_with_empty_name_with_space(self):
        empty_name = " "
        email = "any_email@mail.com"

        with pytest.raises(ValueError) as excinfo:
            Customer.create(name=empty_name, email=email)

        assert "Name cannot be empty" in str(excinfo.value)

    def test_customer_with_less_than_3_chars(self):
        short_name = "ab"
        email = "any_email@mail.com"

        with pytest.raises(ValueError) as excinfo:
            Customer.create(name=short_name, email=email)

        assert "Name must have at least 3 characters" in str(excinfo.value)

    def test_customer_with_invalid_email(self):
        name = "Any Name"
        invalid_email = "invalid-email"

        with pytest.raises(ValueError) as excinfo:
            Customer.create(name=name, email=invalid_email)

        assert "Invalid email format" in str(excinfo.value)

    def test_update_customer_data(self):
        customer = Customer.create(name="original_name", email="original@mail.com")

        customer.update(name="new_name", email="new@mail.com")

        assert customer.name == "new_name"
        assert customer.email == "new@mail.com"
        assert customer.updated_at > customer.created_at

    def test_update_customer_data_with_only_name(self):
        customer = Customer.create(name="original_name", email="original@mail.com")

        customer.update(name="new_name")

        assert customer.name == "new_name"
        assert customer.email == "original@mail.com"

    def test_update_customer_data_with_only_email(self):
        customer = Customer.create(name="original_name", email="original@mail.com")

        customer.update(email="new@mail.com")

        assert customer.name == "original_name"
        assert customer.email == "new@mail.com"

    def test_validate_name_on_update_method(self):

        with pytest.raises(ValueError) as excinfo:
            customer = Customer.create(name="original_name", email="original@mail.com")

            customer.update(name="ab", email="new@mail.com")

        assert "Name must have at least 3 characters" in str(excinfo.value)

    def test_validate_email_on_update_method(self):

        with pytest.raises(ValueError) as excinfo:
            customer = Customer.create(name="original_name", email="original@mail.com")

            customer.update(name="new_name", email="invalid-email")

        assert "Invalid email format" in str(excinfo.value)

    def test_load_existing_customer(self):
        customer_id = uuid.uuid4()
        created_at = datetime.now() - timedelta(days=5)
        updated_at = datetime.now() - timedelta(days=2)
        deleted_at = datetime.now() - timedelta(days=1)
        
        customer = Customer.load(
            id=customer_id,
            name="any_name",
            email="any_email@mail.com",
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )
        
        assert customer.id == customer_id
        assert customer.name == "any_name"
        assert customer.email == "any_email@mail.com"
        assert customer.created_at == created_at
        assert customer.updated_at == updated_at
        assert customer.deleted_at == deleted_at
        assert customer.is_deleted is True

    def test_customer_soft_delete(self):
        customer = Customer.create(
            name="any_name",
            email="any_email@mail.com"
        )
        assert customer.is_deleted is False
        assert customer.deleted_at is None
        
        customer.delete()
        
        assert customer.is_deleted is True
        assert isinstance(customer.deleted_at, datetime)
        
        assert customer.name == "any_name"
        assert customer.email == "any_email@mail.com"

    def test_customer_to_dict(self):
        customer_id = uuid.uuid4()
        customer = Customer(
            id=customer_id,
            name="any_name", 
            email="any_email@mail.com"
        )
        
        result = customer.to_dict()
        
        assert isinstance(result, dict)
        assert result["id"] == str(customer_id)
        assert result["name"] == "any_name"
        assert result["email"] == "any_email@mail.com"
        assert "created_at" in result
        assert "updated_at" in result
        assert "deleted_at" in result

    def test_create_from_dict(self):
        data = {
            "name": "any_name",
            "email": "any_email@mail.com"
        }
        
        customer = Customer.from_dict(data)
        
        assert customer.name == "any_name"
        assert customer.email == "any_email@mail.com"
        assert isinstance(customer.id, uuid.UUID) 