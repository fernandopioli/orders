from src.shared.domain.errors import ValidationError

class TestValidationError:
    def test_validation_error_creation(self):
        error = ValidationError("Invalid value", "field1", "CUSTOM_CODE")
        
        assert error.message == "Invalid value"
        assert error.field == "field1"
        assert error.code == "CUSTOM_CODE"
    
    def test_validation_error_default_code(self):
        error = ValidationError("Invalid value", "field1")
        
        assert error.code == "VALIDATION_ERROR"
    
    def test_str_representation_with_field(self):
        error = ValidationError("Invalid value", "field1", "CODE")
        
        assert str(error) == "CODE: field1 - Invalid value"
    
    def test_str_representation_without_field(self):
        error = ValidationError("General error", code="CODE")
        
        assert str(error) == "CODE: General error"
    
    def test_equality(self):
        error1 = ValidationError("Invalid", "field", "CODE")
        error2 = ValidationError("Invalid", "field", "CODE")
        error3 = ValidationError("Different", "field", "CODE")
        
        assert error1 == error2
        assert error1 != error3
        assert error1 != "Not an error object" 