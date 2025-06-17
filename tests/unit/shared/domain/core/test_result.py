import pytest

from src.shared.domain.core import Result


class TestResult:
    def test_result_success(self):
        value = "test_value"

        result = Result.ok(value)

        assert result.success is True
        assert result.failure is False
        assert result.value == value

    def test_result_failure(self):
        errors = [Exception("Error 1"), Exception("Error 2")]

        result = Result.fail(errors)

        assert result.success is False
        assert result.failure is True
        assert result.errors == errors

    def test_accessing_value_on_failure_raises_exception(self):
        result = Result.fail([Exception("Error")])

        with pytest.raises(ValueError):
            result.value

    def test_bool_conversion(self):
        success_result = Result.ok("value")
        failure_result = Result.fail([Exception("Error")])

        assert bool(success_result) is True
        assert bool(failure_result) is False

        if success_result:
            assert True
        else:
            assert False

        if failure_result:
            assert False
        else:
            assert True
