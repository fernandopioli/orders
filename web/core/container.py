from typing import Dict, Any, TypeVar, Type

from src.order.application.usecases import CreateOrderUseCase
from src.order.main import UseCaseFactory

T = TypeVar('T')

class DIContainer:
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        self.register(CreateOrderUseCase, UseCaseFactory.create_order_use_case())
    
    def register(self, interface: Type[T], implementation: T) -> None:
        self._services[interface] = implementation
    
    def resolve(self, interface: Type[T]) -> T:
        service = self._services.get(interface)
        if service is None:
            raise ValueError(f"Service {interface} not registered")
        return service

container = DIContainer()