from typing import Any

from src.shared.domain.validation import ValidationRule
from src.shared.domain.errors import RequiredError, ValidationError

class RequiredRule(ValidationRule):
    def validate(self, value: Any, field_name: str) -> ValidationError | None:
        if value is None:
            return RequiredError(field_name)
            
        if isinstance(value, str) and value.strip() == "":
            return RequiredError(field_name)
            
        # Valida collections vazias (opcional, descomente se necessário)
        # if hasattr(value, "__len__") and len(value) == 0:
        #     return RequiredError(field_name)
            
        return None