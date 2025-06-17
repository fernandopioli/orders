from src.shared.domain.errors.validation_error import ValidationError


class EmailError(ValidationError):
    def __init__(self, field_name: str, current_value: str):
        super().__init__(
            f"The field {field_name} must be a valid email. Current value: {current_value}",
            field_name,
            "EMAIL_FORMAT_ERROR",
        )
