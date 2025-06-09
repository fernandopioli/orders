import uuid
from typing import Dict, Optional

from src.shared.domain.core import Result
from src.order.domain import Order
from src.order.application.ports import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    
    def __init__(self):
        self._orders: Dict[uuid.UUID, Order] = {}
    
    def save(self, order: Order) -> Result[None]:
        try:
            self._orders[order.id] = order
            return Result.ok()
        except Exception as e:
            return Result.fail([e])
    
    def get_by_id(self, order_id: uuid.UUID) -> Result[Optional[Order]]:
        try:
            order = self._orders.get(order_id)
            return Result.ok(order)
        except Exception as e:
            return Result.fail([e])
    
    def clear(self) -> None:
        self._orders.clear()
    
    def count(self) -> int:
        return len(self._orders)
    
    def get_all(self) -> Result[list[Order]]:
        try:
            orders = list(self._orders.values())
            return Result.ok(orders)
        except Exception as e:
            return Result.fail([e]) 