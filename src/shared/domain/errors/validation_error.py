class ValidationError(Exception):
    def __init__(self, message: str, field: str = None, code: str = None):
        self.message = message
        self.field = field
        self.code = code or "VALIDATION_ERROR"
        super().__init__(message)

    def __str__(self) -> str:
        if self.field:
            return f"{self.code}: {self.field} - {self.message}"
        return f"{self.code}: {self.message}"

    def __eq__(self, other):
        if not isinstance(other, ValidationError):
            return False
        return (
            self.message == other.message and self.field == other.field and self.code == other.code
        )
