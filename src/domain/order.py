import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from src.domain.entity import Entity

class Order(Entity):
    def __init__(
        self,   
        customer_id: str, 
        total: float, 
        id: Optional[uuid.UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None
    ):
        self.customer_id = customer_id
        self.total = total
        super().__init__(id, created_at, updated_at, deleted_at)
        

    @classmethod
    def create(cls, customer_id: str, total: float) -> "Order":
        cls.validate(total, customer_id)
        return cls(customer_id, total)
    
    @classmethod
    def load(cls, id: str, customer_id: str, total: float, created_at: datetime, updated_at: datetime, deleted_at: Optional[datetime] = None) -> "Order":
        return cls(customer_id, total, id, created_at, updated_at, deleted_at)  
    
    def delete(self):
        super()._Entity__delete()

    def update_total(self, total: float) -> None:
        self._validate_total(total)
        self.total = total
        super().update()
    
    @staticmethod
    def validate(total, customer_id) -> None:
        if not isinstance(total, (int, float)):
            raise TypeError("Order total must be a number")
        if total <= 0:
            raise ValueError("Order total must be greater than zero")
        if not isinstance(customer_id, uuid.UUID):
            raise TypeError("Customer ID must be a valid UUID")
        
    def _validate_total(self, total: Any) -> None:
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
        customer_id = data.get("customer_id")
        total = data.get("total")
        
        return cls.create(customer_id=uuid.UUID(customer_id), total=total)
