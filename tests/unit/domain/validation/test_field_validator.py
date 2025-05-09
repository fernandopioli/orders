import pytest

from src.domain.validation import ValidationContext
from src.domain.validation.field_validator import FieldValidator
from src.domain.errors import RequiredError, MinLengthError, EmailError, CurrencyError, UUIDFormatError

class TestFieldValidator:
    def test_required_valid(self):
        validator = FieldValidator("value", "field")
        context = ValidationContext()
        
        validator.required()
        validator.validate(context)
        
        assert not context.has_errors()
    
    def test_required_invalid(self):
        empty_values = [
            "",
            " ",
            None
        ]
    
        for value in empty_values:
            validator = FieldValidator(value, "field")
            context = ValidationContext()
            
            validator.required()
            validator.validate(context)
        
            assert context.has_errors()
            assert len(context.get_errors()) == 1
            assert context.get_errors()[0] == RequiredError("field")
    
    def test_min_length_valid(self):
        validator = FieldValidator("abcde", "field")
        context = ValidationContext()
        
        validator.min_length(3)
        validator.validate(context)
        
        assert not context.has_errors()
    
    def test_min_length_invalid(self):
        validator = FieldValidator("ab", "field")
        context = ValidationContext()
        
        validator.min_length(3)
        validator.validate(context)
        
        assert context.has_errors()
        assert len(context.get_errors()) == 1
        assert context.get_errors()[0] == MinLengthError("field", 3, "ab")
    
    def test_email_valid(self):
        valid_emails = [
            "test@example.com",
            "test.email@example.com",
            "test+email@example.com",
            "test-email@example.com",
            "test_email@example.com",
            "test@subdomain.example.com",
            "test@example.co.uk",
            "test@example.museum",
        ]
    
        for value in valid_emails:
            validator = FieldValidator(value, "email")
            context = ValidationContext()
            
            validator.email()
            validator.validate(context)
        
            assert not context.has_errors()
    
    def test_email_invalid(self):
        invalid_emails = [
            "invalid-email",
            "invalid-email@example",
            "invalid-email@example.",
            "invalid-email@.com",
            12
        ]
    
        for value in invalid_emails:
            validator = FieldValidator(value, "email")
            context = ValidationContext()
            
            validator.email()
            validator.validate(context)
        
            assert context.has_errors()
            assert len(context.get_errors()) == 1
            assert context.get_errors()[0] == EmailError("email", value)
    
    def test_currency_valid(self):
        valid_currency = [
            12,
            12.0,
            12.00
        ]
    
        for value in valid_currency:
            validator = FieldValidator(value, "currency")
            context = ValidationContext()
            
            validator.currency()
            validator.validate(context)
        
            assert not context.has_errors()
    
    def test_currency_invalid(self):
        invalid_currency = [
            "invalid-currency",
            0,
            -1,
            12.123
        ]
    
        for value in invalid_currency:
            validator = FieldValidator(value, "currency")
            context = ValidationContext()
            
            validator.currency()
            validator.validate(context)
        
            assert context.has_errors()
            assert len(context.get_errors()) == 1
            assert context.get_errors()[0] == CurrencyError("currency", value)

    def test_uuid_valid(self):
        validator = FieldValidator("123e4567-e89b-12d3-a456-426614174000", "uuid")
        context = ValidationContext()
        
        validator.uuid()
        validator.validate(context)
        
        assert not context.has_errors()
    
    def test_uuid_invalid(self):
        invalid_uuids = [
            "invalid-uuid",
            12
        ]
    
        for value in invalid_uuids:
            validator = FieldValidator(value, "uuid")
            context = ValidationContext()
            
            validator.uuid()
            validator.validate(context)
        
            assert context.has_errors()
            assert len(context.get_errors()) == 1
            assert context.get_errors()[0] == UUIDFormatError("uuid", value)
    
    def test_chaining_all_valid(self):
        validator = FieldValidator("test@example.com", "email")
        context = ValidationContext()
        
        validator.required().email().min_length(3)
        validator.validate(context)
        
        assert not context.has_errors()
    
    def test_chaining_one_invalid(self):
        validator = FieldValidator("a@", "email")
        context = ValidationContext()
        
        validator.required().min_length(3).email()
        validator.validate(context)
        
        assert context.has_errors()
        assert len(context.get_errors()) == 2
        assert context.get_errors()[0] == MinLengthError("email", 3, "a@")
        assert context.get_errors()[1] == EmailError("email", "a@")