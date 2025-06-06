from typing import Any
import re

from src.shared.domain.validation import ValidationRule
from src.shared.domain.errors import EmailError, ValidationError

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