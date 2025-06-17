from rest_framework import status
from rest_framework.response import Response


class ResponseHelper:
    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        response_data = {"success": True, "message": message, "data": data}
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        response_data = {"success": False, "message": message, "errors": errors or []}
        return Response(response_data, status=status_code)
