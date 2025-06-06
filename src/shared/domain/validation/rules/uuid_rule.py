from typing import Any
import uuid

from src.shared.domain.validation import ValidationRule
from src.shared.domain.errors import UUIDFormatError, ValidationError

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