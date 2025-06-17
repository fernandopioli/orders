class CreateOrderInput:
    def __init__(self, customer_id: str | None = None, total: float | None = None):
        self.customer_id = customer_id
        self.total = total

    @classmethod
    def from_dict(cls, data: dict) -> "CreateOrderInput":
        return cls(
            customer_id=data.get("customer_id") if data.get("customer_id") else None,
            total=data.get("total") if data.get("total") else None,
        )
