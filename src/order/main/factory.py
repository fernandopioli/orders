from src.order.application.ports import OrderRepository
from src.order.application.usecases import CreateOrderUseCase
from src.order.infrastructure.repositories import InMemoryOrderRepository
from src.shared.domain.events import DomainEventPublisher
from src.shared.infrastructure.events.handlers import ConsoleLogHandler


class RepositoryFactory:
    @staticmethod
    def order_repository() -> OrderRepository:
        return InMemoryOrderRepository()


class EventFactory:
    @staticmethod
    def domain_event_publisher() -> DomainEventPublisher:
        return DomainEventPublisher()


class UseCaseFactory:
    @staticmethod
    def create_order_use_case() -> CreateOrderUseCase:
        event_publisher = EventFactory.domain_event_publisher()
        event_publisher.subscribe("OrderCreatedEvent", ConsoleLogHandler())
        return CreateOrderUseCase(
            repository=RepositoryFactory.order_repository(),
            domain_event_publisher=event_publisher,
        )
