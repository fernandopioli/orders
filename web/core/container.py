from typing import Dict, Any, TypeVar, Type

from src.order.application.ports import OrderRepository
from src.order.infrastructure.repositories import InMemoryOrderRepository
from src.order.application.usecases import CreateOrderUseCase
from src.shared.domain.events import DomainEventPublisher
from src.order.domain.events import OrderCreatedEvent
from src.shared.infrastructure.events.handlers import ConsoleLogHandler

T = TypeVar('T')

class DIContainer:
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        # Infrastructure
        order_repository = InMemoryOrderRepository()
        event_publisher = DomainEventPublisher()

        
        # Register dependencies
        self.register(OrderRepository, order_repository)
        self.register(DomainEventPublisher, event_publisher)
        
        event_publisher.subscribe("OrderCreatedEvent", ConsoleLogHandler())
        # Application Services
        create_order_use_case = CreateOrderUseCase(
            repository=order_repository,
            domain_event_publisher=event_publisher
        )
        self.register(CreateOrderUseCase, create_order_use_case)
    
    def register(self, interface: Type[T], implementation: T) -> None:
        self._services[interface] = implementation
    
    def resolve(self, interface: Type[T]) -> T:
        service = self._services.get(interface)
        if service is None:
            raise ValueError(f"Service {interface} not registered")
        return service

# Singleton instance
container = DIContainer()