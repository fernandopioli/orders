class CreateOrderInput:
    def __init__(self, customer_id: str, total: float):
        self.customer_id = customer_id
        self.total = total