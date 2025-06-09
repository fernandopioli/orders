import uuid
from abc import ABC, abstractmethod
from typing import Optional

from src.shared.domain.core import Result
from src.order.domain import Order

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Result[None]:
        pass
    
    @abstractmethod
    def get_by_id(self, order_id: uuid.UUID) -> Result[Optional[Order]]:
        pass