from abc import ABC, abstractmethod
from typing import Any

from src.shared.domain.errors import ValidationError


class ValidationRule(ABC):
    @abstractmethod
    def validate(self, value: Any, field_name: str) -> ValidationError | None:
        pass
