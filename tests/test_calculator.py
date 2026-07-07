from decimal import Decimal

from calculator import Calculator, DivisionByZeroError, InvalidExpressionError


def test_add() -> None:
    calc = Calculator()
    assert calc.add(2, 3) == Decimal("5")


def test_subtract() -> None:
    calc = Calculator()
    assert calc.subtract(10, 4.5) == Decimal("5.5")


def test_multiply() -> None:
    calc = Calculator()
    assert calc.multiply(-2, 3) == Decimal("-6")


def test_divide() -> None:
    calc = Calculator()
    assert calc.divide(7.5, 2.5) == Decimal("3")


def test_divide_by_zero_raises() -> None:
    calc = Calculator()
    try:
        calc.divide(5, 0)
        assert False, "Expected DivisionByZeroError"
    except DivisionByZeroError:
        assert True


def test_evaluate_expression() -> None:
    calc = Calculator()
    assert calc.evaluate_expression("-5+2*4") == Decimal("3")


def test_invalid_expression_raises() -> None:
    calc = Calculator()
    try:
        calc.evaluate_expression("2++")
        assert False, "Expected InvalidExpressionError"
    except InvalidExpressionError:
        assert True
