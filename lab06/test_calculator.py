import pytest

from lab06.calculator import Calculator


@pytest.fixture
def calculator():
    return Calculator()


@pytest.mark.parametrize("method,a,b,expected", [
    ("add", 2, 3, 5), ("add", -7, 2, -5), ("add", 0, 0, 0), ("add", 0.1, 0.2, 0.3),
    ("subtract", 7, 10, -3), ("subtract", -4, -2, -2), ("subtract", 0, 0, 0), ("subtract", 1.5, .5, 1),
    ("multiply", 3, 4, 12), ("multiply", -3, 4, -12), ("multiply", 10, 0, 0), ("multiply", .2, .5, .1),
    ("divide", 10, 2, 5), ("divide", -9, 3, -3), ("divide", 0, 5, 0), ("divide", 1, 3, 1/3),
])
def test_arithmetic(calculator, method, a, b, expected):
    assert getattr(calculator, method)(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("numerator", [0, 1, -1, 1.5])
def test_divide_by_zero(calculator, numerator):
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        calculator.divide(numerator, 0)


@pytest.mark.parametrize("number,expected", [(-10,False), (0,False), (1,False), (2,True), (3,True), (4,False), (9,False), (25,False), (29,True), (97,True)])
def test_is_prime_number(calculator, number, expected):
    assert calculator.is_prime_number(number) is expected


@pytest.mark.parametrize("value", [True, 2.5, "7", None])
def test_prime_requires_integer(calculator, value):
    with pytest.raises(TypeError):
        calculator.is_prime_number(value)


@pytest.mark.parametrize("method", ["add", "subtract", "multiply", "divide"])
@pytest.mark.parametrize("value,error", [("2",TypeError), (True,TypeError), (float("nan"),ValueError), (float("inf"),ValueError)])
def test_invalid_operand(calculator, method, value, error):
    with pytest.raises(error):
        getattr(calculator, method)(value, 1)
