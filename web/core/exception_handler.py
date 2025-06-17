from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from src.shared.domain.errors import ValidationError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        return Response(
            {"success": False, "message": "Validation failed", "errors": [str(exc)]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if response is None:
        return Response(
            {
                "success": False,
                "message": "Internal server error",
                "errors": ["An unexpected error occurred"],
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    error_messages = {
        400: "Bad request",
        401: "Unauthorized", 
        404: "Page not found",
        405: "Method not allowed",
        429: "Too many requests",
    }

    message = error_messages.get(response.status_code, "Request failed")

    return Response(
        {
            "success": False,
            "message": message,
            "errors": response.data if isinstance(response.data, list) else [response.data],
        },
        status=response.status_code,
    )
