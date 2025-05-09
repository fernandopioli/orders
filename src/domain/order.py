import uuid
from datetime import datetime
from typing import List, Any, Dict, Optional

from src.domain.core import Entity, Result
from src.domain.validation import Validator
from src.domain.errors import ValidationError

class Order(Entity):
    def __init__(
        self,   
        customer_id: uuid.UUID, 
        total: float, 
        id: uuid.UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        deleted_at: datetime | None = None
    ):
        self.customer_id = customer_id
        self.total = total
        super().__init__(id, created_at, updated_at, deleted_at)

    @classmethod
    def create(cls, customer_id: str, total: float) -> Result["Order"]:
        result = cls.validate(total, customer_id)

        if result.failure:
            return Result.fail(result.errors)
        
        return Result.ok(cls(customer_id, total))
    
    @staticmethod
    def validate(total, customer_id) -> Result[List[ValidationError] | None]:
        validator = Validator()
        
        Order._validate_total(validator, total)
            
        validator.field(customer_id, "customer_id") \
            .required() \
            .uuid()
        
        result = validator.validate()

        if result.failure:
            return Result.fail(result.errors)
        
        return Result.ok()

    @staticmethod
    def _validate_total(validator: Validator, total) -> None:
        validator.field(total, "total") \
        .required() \
        .currency()
        
    @classmethod
    def load(cls, id: str, customer_id: str, total: float, created_at: datetime, updated_at: datetime, deleted_at: Optional[datetime] = None) -> Result["Order"]:
        return Result.ok(cls(id=uuid.UUID(id), customer_id=uuid.UUID(customer_id), total=total, created_at=created_at, updated_at=updated_at, deleted_at=deleted_at))  
    
    def update_total(self, total: float) -> Result[None]:
        result = self.validate_total(total)
        if result.failure:
            return Result.fail(result.errors)
        
        self.total = total
        super().update()
        
        return Result.ok()
    
    def validate_total(self, total) -> Result[List[ValidationError] | None]:
        validator = Validator()
        
        Order._validate_total(validator, total)
        
        result = validator.validate()
        
        if result.failure:
            return Result.fail(result.errors)
        
        return Result.ok()

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "customer_id": str(self.customer_id),
            "total": self.total
        })
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Result["Order"]:
        return cls.load(
            id=data.get("id"),
            customer_id=data.get("customer_id"),
            total=data.get("total"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            deleted_at=data.get("deleted_at")
        )
