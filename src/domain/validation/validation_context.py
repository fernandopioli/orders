from typing import List

from src.domain.errors import ValidationError

class ValidationContext:
    def __init__(self):
        self._errors: List[ValidationError] = []
    
    def add_error(self, error: ValidationError) -> None:
        self._errors.append(error)
    
    def has_errors(self) -> bool:
        return len(self._errors) > 0
    
    def get_errors(self) -> List[ValidationError]:
        return self._errors.copy()
    
    def clear(self) -> None:
        self._errors.clear()

