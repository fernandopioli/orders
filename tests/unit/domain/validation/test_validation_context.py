import pytest

from src.domain.errors import ValidationError
from src.domain.validation import ValidationContext

class TestValidationContext:
    def test_add_error(self):
        context = ValidationContext()
        error = ValidationError("Invalid value", "field1")
        
        context.add_error(error)
        
        assert context.has_errors() is True
        assert len(context.get_errors()) == 1
        assert context.get_errors()[0] == error
    
    def test_has_errors(self):
        context = ValidationContext()
        
        assert context.has_errors() is False
        
        context.add_error(ValidationError("Error"))
        
        assert context.has_errors() is True
    
    def test_get_errors_returns_copy(self):
        context = ValidationContext()
        context.add_error(ValidationError("Error 1"))
        
        errors = context.get_errors()
        errors.append(ValidationError("Error 2"))
        
        assert len(context.get_errors()) == 1
    
    def test_clear(self):
        context = ValidationContext()
        context.add_error(ValidationError("Error 1"))
        context.add_error(ValidationError("Error 2"))
        
        context.clear()
        
        assert context.has_errors() is False
        assert len(context.get_errors()) == 0