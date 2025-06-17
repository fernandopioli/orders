from typing import Any

from src.shared.domain.errors import MinLengthError, ValidationError
from src.shared.domain.validation.validation_rule import ValidationRule


class MinLengthRule(ValidationRule):
    def __init__(self, min_length: int):
        self.min_length = min_length

    def validate(self, value: Any, field_name: str) -> ValidationError | None:
        if value is not None and len(value.strip()) > 0:
            if isinstance(value, str) and len(value.strip()) < self.min_length:
                return MinLengthError(field_name, self.min_length, value)
        return None
