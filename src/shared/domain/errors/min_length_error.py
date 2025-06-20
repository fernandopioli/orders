from src.shared.domain.errors.validation_error import ValidationError


class MinLengthError(ValidationError):
    def __init__(self, field_name: str, min_length: int, current_value: str):
        super().__init__(
            (
                f"The field {field_name} must have at least {min_length} characters. "
                f"Current value: {current_value}"
            ),
            field_name,
            "MIN_LENGTH_ERROR",
        )
