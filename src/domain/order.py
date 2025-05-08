import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from src.domain.entity import Entity

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
    def create(cls, customer_id: str, total: float) -> "Order":
        cls.validate(total, customer_id)
        return cls(customer_id, total)
    
    @staticmethod
    def validate(total, customer_id) -> None:
        if not isinstance(total, (int, float)):
            raise TypeError("Order total must be a number")
        if total <= 0:
            raise ValueError("Order total must be greater than zero")
        try:
            uuid.UUID(customer_id)
        except (ValueError, TypeError):
            raise TypeError("Customer ID must be a valid UUID")
        
    @classmethod
    def load(cls, id: str, customer_id: str, total: float, created_at: datetime, updated_at: datetime, deleted_at: Optional[datetime] = None) -> "Order":
        return cls(id=uuid.UUID(id), customer_id=uuid.UUID(customer_id), total=total, created_at=created_at, updated_at=updated_at, deleted_at=deleted_at)  
    
    def update_total(self, total: float) -> None:
        self.validate_total(total)
        self.total = total
        super().update()
    
    def validate_total(self, total) -> None:
        if not isinstance(total, (int, float)):
            raise TypeError("Order total must be a number")
        if total <= 0:
            raise ValueError("Order total must be greater than zero")

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "customer_id": str(self.customer_id),
            "total": self.total
        })
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        return cls.load(
            id=data.get("id"),
            customer_id=data.get("customer_id"),
            total=data.get("total"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            deleted_at=data.get("deleted_at")
        )
