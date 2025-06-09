from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from web.core.container import container
from src.order.application.usecases import CreateOrderUseCase
from .serializers import (
    CreateOrderRequestSerializer,
    OrderResponseSerializer,
)


class CreateOrderAPIView(APIView):
    
    def post(self, request):
        # 1. Validate request data
        request_serializer = CreateOrderRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return self._error_response(
                message="Validation failed",
                errors=request_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # 2. Convert to DTO
        input_dto = request_serializer.to_dto()
        
        # 3. Execute use case
        use_case = container.resolve(CreateOrderUseCase)
        result = use_case.execute(input_dto)
        
        # 4. Handle result
        if result.failure:
            return self._error_response(
                message="Failed to create order",
                errors=[str(error) for error in result.errors],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # 5. Success response
        order_data = OrderResponseSerializer(result.value).instance
        return self._success_response(
            data={"order": order_data},
            message="Order created successfully",
            status_code=status.HTTP_201_CREATED
        )
    
    def _success_response(self, data=None, message="Success", status_code=status.HTTP_200_OK):
        response_data = {
            "success": True,
            "data": data,
            "message": message
        }
        return Response(response_data, status=status_code)
    
    def _error_response(self, message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        response_data = {
            "success": False,
            "message": message,
            "errors": errors or []
        }
        return Response(response_data, status=status_code)