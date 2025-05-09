import pytest

from src.domain.validation import Validator
from src.domain.validation.field_validator import FieldValidator

class TestValidator:
    def test_validate_all_fields_valid(self):
        validator = Validator()
        
        validator.field("John", "name").required().min_length(3)
        validator.field("john@example.com", "email").required().email()
        result = validator.validate()
        
        assert result.success is True
        assert result.value is True
    
    def test_validate_one_field_invalid(self):
        validator = Validator()
        
        validator.field("John", "name").required().min_length(3)
        validator.field("invalid-email", "email").required().email()
        result = validator.validate()
        
        assert result.success is False
        assert len(result.errors) == 1
        assert result.errors[0].field == "email"
    
    def test_validate_multiple_fields_invalid(self):
        validator = Validator()
        
        validator.field("", "name").required()
        validator.field("invalid", "email").email()
        result = validator.validate()
        
        assert result.success is False
        assert len(result.errors) == 2
            
    def test_field_returns_field_validator(self):
        validator = Validator()
        
        field_validator = validator.field("value", "field")
        
        assert isinstance(field_validator, FieldValidator)
        assert field_validator.value == "value"
        assert field_validator.field_name == "field"
    
    def test_reusing_validator(self):
        validator = Validator()
        validator.field("John", "name").required()
        
        result1 = validator.validate()
        assert result1.success is True
        
        validator.field("", "email").required()
        result2 = validator.validate()
        
        assert result2.success is False
        assert len(result2.errors) == 1 

        validator.field("Jo", "name").min_length(3)
        result3 = validator.validate()
        
        assert result3.success is False
        assert len(result3.errors) == 2 

