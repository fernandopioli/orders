from src.order.application.dtos import CreateOrderInput, CreateOrderOutput
from src.order.application.ports import OrderRepository
from src.order.domain import Order
from src.order.domain.events import OrderCreatedEvent
from src.shared.application import UseCase
from src.shared.domain.core import Result
from src.shared.domain.events import DomainEventPublisher


class CreateOrderUseCase(UseCase[CreateOrderInput, CreateOrderOutput]):
    def __init__(self, repository: OrderRepository, domain_event_publisher: DomainEventPublisher):
        self.repository = repository
        self.domain_event_publisher = domain_event_publisher

    def execute(self, input: CreateOrderInput) -> Result[CreateOrderOutput]:
        order = Order.create(customer_id=input.customer_id, total=input.total)
        if order.failure:
            return Result.fail(order.errors)

        result = self.repository.save(order.value)
        if result.failure:
            return Result.fail(result.errors)

        self.domain_event_publisher.publish([OrderCreatedEvent(order.value)])

        return Result.ok(CreateOrderOutput(order.value))
