from src.order.domain import Order

class CreateOrderOutput:
    def __init__(self, order: Order):
        self.order = order