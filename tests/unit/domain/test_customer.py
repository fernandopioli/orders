import pytest
import uuid
from datetime import datetime, timedelta

from src.domain.customer import Customer
from src.domain.errors import RequiredError, MinLengthError, EmailError

class TestCustomer:

    def test_create_customer_with_valid_data(self):
        name = "Any name"
        email = "any_email@mail.com"

        result = Customer.create(name=name, email=email)

        assert result.success is True
        assert isinstance(result.value, Customer)
        assert isinstance(result.value.id, uuid.UUID)
        assert result.value.name == name
        assert result.value.email == email
        assert isinstance(result.value.created_at, datetime)
        assert isinstance(result.value.updated_at, datetime)
        assert result.value.deleted_at is None
        assert result.value.is_deleted is False

    def test_customer_with_empty_name(self):
        empty_name = ""
        email = "any_email@mail.com"

        result = Customer.create(name=empty_name, email=email)

        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors[0] == RequiredError("name")

    def test_customer_with_less_than_3_chars(self):
        short_name = "ab"
        email = "any_email@mail.com"

        result = Customer.create(name=short_name, email=email)

        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors[0] == MinLengthError("name", 3, short_name)

    def test_customer_with_empty_email(self):
        name = "Any Name"
        empty_email = ""

        result = Customer.create(name=name, email=empty_email)

        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors[0] == RequiredError("email")

    def test_customer_with_invalid_email(self):
        name = "Any Name"
        invalid_email = "invalid-email"

        result = Customer.create(name=name, email=invalid_email)

        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors[0] == EmailError("email", invalid_email)

    def test_update_customer_data(self):
        customer = Customer.create(name="original_name", email="original@mail.com").value

        customer.update(name="new_name", email="new@mail.com")

        assert customer.name == "new_name"
        assert customer.email == "new@mail.com"
        assert customer.updated_at > customer.created_at

    def test_update_customer_data_with_only_name(self):
        customer = Customer.create(name="original_name", email="original@mail.com").value

        customer.update(name="new_name")

        assert customer.name == "new_name"
        assert customer.email == "original@mail.com"

    def test_update_customer_data_with_only_email(self):
        customer = Customer.create(name="original_name", email="original@mail.com").value

        customer.update(email="new@mail.com")

        assert customer.name == "original_name"
        assert customer.email == "new@mail.com"

    def test_validate_name_on_update_method(self):

        customer = Customer.create(name="original_name", email="original@mail.com").value

        result = customer.update(name="ab", email="new@mail.com")

        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors[0] == MinLengthError("name", 3, "ab")

    def test_validate_email_on_update_method(self):

        customer = Customer.create(name="original_name", email="original@mail.com").value

        result = customer.update(name="new_name", email="invalid-email")

        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors[0] == EmailError("email", "invalid-email")

    def test_load_existing_customer(self):
        customer_id = uuid.uuid4()
        created_at = datetime.now() - timedelta(days=5)
        updated_at = datetime.now() - timedelta(days=2)
        deleted_at = datetime.now() - timedelta(days=1)
        
        result = Customer.load(
            id=str(customer_id),
            name="any_name",
            email="any_email@mail.com",
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )
        
        assert result.success is True
        assert isinstance(result.value, Customer)
        assert result.value.id == customer_id
        assert result.value.name == "any_name"
        assert result.value.email == "any_email@mail.com"
        assert result.value.created_at == created_at
        assert result.value.updated_at == updated_at
        assert result.value.deleted_at == deleted_at
        assert result.value.is_deleted is True

    def test_customer_soft_delete(self):
        customer = Customer.create(
            name="any_name",
            email="any_email@mail.com"
        ).value
        assert customer.is_deleted is False
        assert customer.deleted_at is None
        
        customer.delete()
        
        assert customer.is_deleted is True
        assert isinstance(customer.deleted_at, datetime)
        
        assert customer.name == "any_name"
        assert customer.email == "any_email@mail.com"

    def test_customer_to_dict(self):
        customer_id = uuid.uuid4()
        customer = Customer.load(
            id=str(customer_id),
            name="any_name", 
            email="any_email@mail.com",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=datetime.now()
        ).value
        
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
            "id": str(uuid.uuid4()),
            "name": "any_name",
            "email": "any_email@mail.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "deleted_at": datetime.now()
        }
        
        result = Customer.from_dict(data)
        
        assert result.success is True
        assert isinstance(result.value, Customer)
        assert result.value.name == "any_name"
        assert result.value.email == "any_email@mail.com"
        assert str(result.value.id) == data["id"]
        assert result.value.created_at == data["created_at"]
        assert result.value.updated_at == data["updated_at"]
        assert result.value.deleted_at == data["deleted_at"]
