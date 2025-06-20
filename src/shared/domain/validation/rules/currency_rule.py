from decimal import ROUND_DOWN, Decimal
from typing import Any

from src.shared.domain.errors import CurrencyError, ValidationError
from src.shared.domain.validation.validation_rule import ValidationRule


class CurrencyRule(ValidationRule):
    def validate(self, value: Any, field_name: str) -> ValidationError | None:
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return None

        if not isinstance(value, (int, float)):
            return CurrencyError(field_name, value)

        if value <= 0:
            return CurrencyError(field_name, value)

        if isinstance(value, float):
            decimal_value = Decimal(str(value))
            truncated = decimal_value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

            if decimal_value != truncated:
                return CurrencyError(field_name, value)

        return None
