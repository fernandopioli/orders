import uuid
from typing import Any

from src.shared.domain.errors import UUIDFormatError, ValidationError
from src.shared.domain.validation.validation_rule import ValidationRule


class UUIDRule(ValidationRule):
    def validate(self, value: Any, field_name: str) -> ValidationError | None:
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return None

        try:
            if isinstance(value, str):
                uuid.UUID(value)
            elif not isinstance(value, uuid.UUID):
                return UUIDFormatError(field_name, value)
        except ValueError:
            return UUIDFormatError(field_name, value)

        return None
