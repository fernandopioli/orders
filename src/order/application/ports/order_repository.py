import uuid
from abc import ABC, abstractmethod
from typing import Optional

from src.order.domain import Order
from src.shared.domain.core import Result


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Result[None]:
        pass

    @abstractmethod
    def get_by_id(self, order_id: uuid.UUID) -> Result[Optional[Order]]:
        pass
