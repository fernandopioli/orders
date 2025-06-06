from src.shared.domain.errors import ValidationError

class RequiredError(ValidationError):
    def __init__(self, field_name: str):
        super().__init__(
            f"The field {field_name} is required", 
            field_name,
            "REQUIRED_ERROR"
        )
        
        