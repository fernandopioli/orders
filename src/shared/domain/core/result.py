from typing import Any, Generic, List, TypeVar

T = TypeVar("T")


class Result(Generic[T]):
    def __init__(
        self,
        value: T | None = None,
        success: bool = True,
        errors: List[Any] | None = None,
    ):
        self._value = value
        self._success = success
        self._errors = errors or []

    @property
    def success(self) -> bool:
        return self._success

    @property
    def failure(self) -> bool:
        return not self._success

    @property
    def value(self) -> T:
        if not self._success:
            raise ValueError("Cannot access value on failure result")
        return self._value

    @property
    def errors(self) -> List[Exception]:
        return self._errors.copy()

    @staticmethod
    def ok(value: T = None) -> "Result[T]":
        return Result(value=value, success=True)

    @staticmethod
    def fail(errors: List[Exception]) -> "Result[Any]":
        return Result(value=None, success=False, errors=errors)

    def __bool__(self) -> bool:
        return self._success
