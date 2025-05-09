from src.domain.errors import ValidationError

class CurrencyError(ValidationError):
    def __init__(self, field_name: str, current_value: str):
        super().__init__(
            f"The field {field_name} must be a valid currency. Current value: {current_value}", 
            field_name,
            "CURRENCY_ERROR"
        )
        
        