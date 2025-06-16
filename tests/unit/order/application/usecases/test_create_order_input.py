from src.order.application.dtos import CreateOrderInput

class TestCreateOrderInput:
    def test_from_dict(self):
        data = {
            'customer_id': '123',
            'total': 100.0
        }
        input_dto = CreateOrderInput.from_dict(data)
        assert input_dto.customer_id == '123'
        assert input_dto.total == 100.0

    def test_from_dict_without_data(self):
        data = {}
        input_dto = CreateOrderInput.from_dict(data)
        assert input_dto.customer_id is None
        assert input_dto.total is None