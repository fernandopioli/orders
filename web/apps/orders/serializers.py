from rest_framework import serializers

from src.order.application.dtos import CreateOrderInput, CreateOrderOutput


class CreateOrderRequestSerializer(serializers.Serializer):
    customer_id = serializers.CharField()
    total = serializers.FloatField()

    def to_dto(self) -> CreateOrderInput:
        return CreateOrderInput(
            customer_id=self.validated_data["customer_id"],
            total=self.validated_data["total"],
        )


class OrderResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    customer_id = serializers.CharField()
    total = serializers.FloatField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def __init__(self, output_dto: CreateOrderOutput, *args, **kwargs):
        super().__init__(*args, **kwargs)
        order = output_dto.order
        self.instance = {
            "id": str(order.id),
            "customer_id": str(order.customer_id),
            "total": order.total,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
        }


class APIResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    data = serializers.DictField(required=False)
    message = serializers.CharField(required=False)
    errors = serializers.ListField(required=False)
