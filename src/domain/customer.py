import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from src.domain.entity import Entity

class Customer(Entity):

    MIN_NAME_LENGTH = 3

    def __init__(
        self,
        name: str,
        email: str,
        id: uuid.UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        deleted_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at, deleted_at)
        self.name = name
        self.email = email

    @classmethod
    def create(
        cls,
        name: str,
        email: str
    ) -> "Customer":
        cls.validate(name, email)
        return cls(
            name=name,
            email=email
        )
    
    @staticmethod
    def validate(name, email) -> None:
        if not name or name.strip() == "":
            raise ValueError("Name cannot be empty")
        if len(name.strip()) < Customer.MIN_NAME_LENGTH:
            raise ValueError("Name must have at least 3 characters")
        if not email or "@" not in email:
            raise ValueError("Invalid email format")

    @classmethod
    def load(
        cls,
        id: str,
        name: str,
        email: str,
        created_at: datetime,
        updated_at: datetime,
        deleted_at: datetime | None = None,
    ) -> "Customer":
        return cls(
            id=uuid.UUID(id),
            name=name,
            email=email,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )
    
    def update(self, name: str | None = None, email: str | None = None) -> None:
        self.validate_on_update(name, email)
        if name:
            self.name = name
        if email:
            self.email = email
        super().update()

    def validate_on_update(self, name: str | None = None, email: str | None = None) -> None:
        if name:
            if len(name.strip()) < Customer.MIN_NAME_LENGTH:
                raise ValueError("Name must have at least 3 characters")
        if email:
            if "@" not in email:
                raise ValueError("Invalid email format")
            
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            "name": self.name,
            "email": self.email
        })
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Customer":
        return cls.load(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            deleted_at=data.get("deleted_at")
        )
