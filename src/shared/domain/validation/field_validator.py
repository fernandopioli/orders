from typing import Any, List

from src.shared.domain.validation.rules import (
    CurrencyRule,
    EmailRule,
    MinLengthRule,
    RequiredRule,
    UUIDRule,
)
from src.shared.domain.validation.validation_context import ValidationContext
from src.shared.domain.validation.validation_rule import ValidationRule


class FieldValidator:
    def __init__(self, value: Any, field_name: str):
        self.value = value
        self.field_name = field_name
        self.rules: List[ValidationRule] = []

    def add_rule(self, rule: ValidationRule) -> "FieldValidator":
        self.rules.append(rule)
        return self

    def required(self) -> "FieldValidator":
        return self.add_rule(RequiredRule())

    def min_length(self, min_length: int) -> "FieldValidator":
        return self.add_rule(MinLengthRule(min_length))

    def email(self) -> "FieldValidator":
        return self.add_rule(EmailRule())

    def uuid(self) -> "FieldValidator":
        return self.add_rule(UUIDRule())

    def currency(self) -> "FieldValidator":
        return self.add_rule(CurrencyRule())

    def validate(self, context: ValidationContext) -> None:
        for rule in self.rules:
            error = rule.validate(self.value, self.field_name)
            if error:
                context.add_error(error)
