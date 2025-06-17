from rest_framework import status
from rest_framework.views import APIView

from src.order.application.dtos import CreateOrderInput
from src.order.application.usecases import CreateOrderUseCase
from web.core.container import container
from web.core.response_utils import ResponseHelper


class OrderAPIView(APIView):
    def post(self, request):
        ev = 1
        if not request.data:
            return ResponseHelper.error(
                message="Request body is required",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        input_dto = CreateOrderInput.from_dict(request.data)

        use_case = container.resolve(CreateOrderUseCase)
        result = use_case.execute(input_dto)

        if result.failure:
            return ResponseHelper.error(
                message="Failed to create order",
                errors=[str(error) for error in result.errors],
            )

        order_data = result.value.order.to_dict()

        return ResponseHelper.success(
            data={"order": order_data},
            message="Order created successfully",
            status_code=status.HTTP_201_CREATED,
        )
