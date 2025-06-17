from src.shared.domain.errors.validation_error import ValidationError


class UUIDFormatError(ValidationError):
    def __init__(self, field_name: str, current_value: str):
        super().__init__(
            f"The field {field_name} must be a valid UUID. Current value: {current_value}",
            field_name,
            "UUID_FORMAT_ERROR",
        )
