import uuid
from datetime import datetime
from typing import Any, Dict, List

from src.domain.core import Entity, Result
from src.domain.validation import Validator
from src.domain.errors import ValidationError

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
    ) -> Result["Customer"]:
        result = cls.validate(name, email)
        if result.failure:
            return Result.fail(result.errors)
        
        return Result.ok(cls(
            name=name,
            email=email
        ))
    
    @staticmethod
    def validate(name, email) -> Result[List[ValidationError] | None]:      
        validator = Validator()
        
        validator.field(name, "name") \
            .required() \
            .min_length(3)
            
        validator.field(email, "email") \
            .required() \
            .email()
        
        result = validator.validate()

        if result.failure:
            return Result.fail(result.errors)
        
        return Result.ok()

    @classmethod
    def load(
        cls,
        id: str,
        name: str,
        email: str,
        created_at: datetime,
        updated_at: datetime,
        deleted_at: datetime | None = None,
    ) -> Result["Customer"]:
        return Result.ok(cls(
            id=uuid.UUID(id),
            name=name,
            email=email,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        ))
    
    def update(self, name: str | None = None, email: str | None = None) -> Result[None]:
        result = self.validate_on_update(name, email)
        if result.failure:
            return Result.fail(result.errors)
        
        if name:
            self.name = name
        if email:
            self.email = email
        super().update()
        
        return Result.ok()

    def validate_on_update(self, name: str | None = None, email: str | None = None) -> Result[List[ValidationError] | None]:  
        validator = Validator()
        
        if name:
            validator.field(name, "name") \
                .min_length(3)
                
        if email:
            validator.field(email, "email") \
                .email()
                
        result = validator.validate()

        if result.failure:
            return Result.fail(result.errors)
        return Result.ok()
            
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            "name": self.name,
            "email": self.email
        })
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Result["Customer"]:
        return cls.load(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            deleted_at=data.get("deleted_at")
        )
