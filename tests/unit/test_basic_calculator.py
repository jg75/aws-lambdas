"""Tests for the BasicCalculatorHandler."""
import pytest

from cf.basic_calculator import handler


@pytest.mark.unit
@pytest.mark.parametrize(
    "operator, operands, value",
    [("+", ["1"], 1), ("+", ["1", "2"], 3), ("+", ["1", "2", "3"], 6),],
)
def test_add(operator, operands, value):
    """It should be able to add."""
    assert handler.execute(operator, operands) == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "operator, operands, value",
    [("-", ["1"], 1), ("-", ["1", "2"], -1), ("-", ["1", "2", "3"], -4),],
)
def test_subtract(operator, operands, value):
    """It should be able to subtract."""
    assert handler.execute(operator, operands) == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "operator, operands, value",
    [
        ("*", ["1"], 1),
        ("*", ["1", "2"], 2),
        ("*", ["1", "2", "3"], 6),
        ("*", ["1", "2", "3", "4"], 24),
    ],
)
def test_multiply(operator, operands, value):
    """It should be able to multiply."""
    assert handler.execute(operator, operands) == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "operator, operands, value",
    [("/", ["1"], 1), ("/", ["2", "2"], 1), ("/", ["12", "3", "2"], 2),],
)
def test_divide(operator, operands, value):
    """It should be able to divide."""
    assert handler.execute(operator, operands) == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "operator, operands, value",
    [("%", ["1"], 1), ("%", ["2", "2"], 0), ("%", ["12", "3", "2"], 0),],
)
def test_modulus(operator, operands, value):
    """It should be able to mod."""
    assert handler.execute(operator, operands) == value
