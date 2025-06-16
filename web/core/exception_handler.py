from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

from src.shared.domain.errors import ValidationError


def exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, ValidationError):
        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": [str(exc)]
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if response is None:
        return Response({
            "success": False,
            "message": "Internal server error", 
            "errors": ["An unexpected error occurred"]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        "success": False,
        "message": "Request failed",
        "errors": response.data if isinstance(response.data, list) else [response.data]
    }, status=response.status_code)