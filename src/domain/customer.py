import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from src.domain.entity import Entity


class Customer(Entity):

    def __init__(
        self,
        name: str,
        email: str,
        id: Optional[uuid.UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
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

    def update(self, name: Optional[str] = None, email: Optional[str] = None):
        self.validate_on_update(name, email)
        if name:
            self.name = name
        if email:
            self.email = email
        
        super().update()

    @classmethod
    def load(
        cls,
        id: uuid.UUID,
        name: str,
        email: str,
        created_at: datetime,
        updated_at: datetime,
        deleted_at: Optional[datetime] = None,
    ) -> "Customer":
        return cls(
            id=id,
            name=name,
            email=email,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )
    
    @staticmethod
    def validate(name: str, email: str):
        if not name or name.strip() == "":
            raise ValueError("Name cannot be empty")
        if len(name.strip()) < 3:
            raise ValueError("Name must have at least 3 characters")
        if not email or "@" not in email:
            raise ValueError("Invalid email format")
        
    def validate_on_update(self, name: Optional[str] = None, email: Optional[str] = None):
        if name:
            if len(name.strip()) < 3:
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
        name = data.get("name")
        email = data.get("email")
        
        return cls.create(name=name, email=email)
