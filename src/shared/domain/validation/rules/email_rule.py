import re
from typing import Any

from src.shared.domain.errors import EmailError, ValidationError
from src.shared.domain.validation.validation_rule import ValidationRule


class EmailRule(ValidationRule):
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def validate(self, value: Any, field_name: str) -> ValidationError | None:
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return None

        if not isinstance(value, str):
            return EmailError(field_name, value)

        if not self.EMAIL_PATTERN.match(value):
            return EmailError(field_name, value)

        return None
