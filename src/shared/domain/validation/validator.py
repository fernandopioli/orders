from typing import Any, List

from src.shared.domain.core.result import Result
from src.shared.domain.validation.validation_context import ValidationContext
from src.shared.domain.validation.field_validator import FieldValidator

class Validator:
    def __init__(self):
        self.context = ValidationContext()
        self.field_validators: List[FieldValidator] = []
    
    def field(self, value: Any, field_name: str) -> FieldValidator:
        field_validator = FieldValidator(value, field_name)
        self.field_validators.append(field_validator)
        return field_validator
    
    def validate(self) -> Result[bool]:
        for validator in self.field_validators:
            validator.validate(self.context)

        if self.context.has_errors():
            errors = self.context.get_errors()
            self.context.clear()
            return Result.fail(errors)
        
        return Result.ok(True)