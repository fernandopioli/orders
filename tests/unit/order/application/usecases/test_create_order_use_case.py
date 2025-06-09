import uuid
import pytest
from unittest.mock import Mock

from src.shared.application import UseCase
from src.shared.domain.core import Result
from src.shared.domain.errors import UUIDFormatError
from src.shared.domain.events import DomainEventPublisher
from src.order.domain import Order
from src.order.domain.events import OrderCreatedEvent
from src.order.application.ports import OrderRepository
from src.order.application.usecases import CreateOrderUseCase
from src.order.application.dtos import CreateOrderInput, CreateOrderOutput

class TestCreateOrderUseCase:

    @pytest.fixture
    def repository(self) -> OrderRepository:
        mock_repo = Mock(spec=OrderRepository)
        mock_repo.save.return_value = Result.ok()
        return mock_repo
    
    @pytest.fixture
    def domain_event_publisher(self) -> DomainEventPublisher:
        mock_publisher = Mock(spec=DomainEventPublisher)
        mock_publisher.publish.return_value = None
        return mock_publisher

    @pytest.fixture
    def create_order_use_case(self, repository: OrderRepository, domain_event_publisher: DomainEventPublisher) -> CreateOrderUseCase:
        return CreateOrderUseCase(repository=repository, domain_event_publisher=domain_event_publisher)

    def test_create_order_use_case_is_use_case_instance(self, create_order_use_case: CreateOrderUseCase):
        assert isinstance(create_order_use_case, UseCase)
    
    def test_create_order_use_case_execute_with_valid_input(self, create_order_use_case: CreateOrderUseCase):
        customer_id = str(uuid.uuid4())
        
        input = CreateOrderInput(customer_id=customer_id, total=100)

        result = create_order_use_case.execute(input)

        assert result.success is True
        assert isinstance(result.value, CreateOrderOutput)
        assert isinstance(result.value.order, Order)
        assert result.value.order.customer_id == customer_id
        assert result.value.order.total == 100

    def test_create_order_use_case_execute_with_invalid_input(self, create_order_use_case: CreateOrderUseCase):
        input = CreateOrderInput(customer_id="invalid", total=100)

        result = create_order_use_case.execute(input)

        assert result.success is False
        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors is not None
        assert result.errors[0] == UUIDFormatError(field_name="customer_id", current_value="invalid")

    def test_create_order_use_case_should_call_repository_with_valid_input(self, create_order_use_case: CreateOrderUseCase):
        customer_id = str(uuid.uuid4())

        input = CreateOrderInput(customer_id=customer_id, total=100)

        create_order_use_case.execute(input)

        create_order_use_case.repository.save.assert_called_once()
        args, _ = create_order_use_case.repository.save.call_args
        assert isinstance(args[0], Order)
        assert args[0].id is not None
        assert args[0].customer_id == customer_id
        assert args[0].total == 100

    def test_create_order_use_case_should_return_failure_when_repository_fails(self, create_order_use_case: CreateOrderUseCase):
        customer_id = str(uuid.uuid4())
        create_order_use_case.repository.save.return_value = Result.fail([Exception("Repository failed")])

        input = CreateOrderInput(customer_id=customer_id, total=100)

        result = create_order_use_case.execute(input)

        assert result.success is False
        assert result.failure is True
        assert len(result.errors) == 1
        assert result.errors is not None
        assert isinstance(result.errors[0], Exception)
        assert str(result.errors[0]) == "Repository failed"

    def test_create_order_use_case_should_call_domain_event_publisher_with_valid_input(self, create_order_use_case: CreateOrderUseCase):
        customer_id = str(uuid.uuid4())

        input = CreateOrderInput(customer_id=customer_id, total=100)

        create_order_use_case.execute(input)

        create_order_use_case.domain_event_publisher.publish.assert_called_once()
        args, _ = create_order_use_case.domain_event_publisher.publish.call_args
        assert len(args[0]) == 1
        assert isinstance(args[0][0], OrderCreatedEvent)