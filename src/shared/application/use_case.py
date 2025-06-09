from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.shared.domain.core import Result

TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')

class UseCase(ABC, Generic[TInput, TOutput]):
    @abstractmethod
    def execute(self, input: TInput) -> Result[TOutput]:
        pass