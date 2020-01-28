import pytest

from src.cf.basic_calculator import handler


@pytest.mark.unit
@pytest.mark.parametrize(
    "operator, operands, value",
    [("+", ["1"], 1), ("+", ["1", "2"], 3), ("+", ["1", "2", "3"], 6),],
)
def test_add(operator, operands, value):
    assert handler.execute(operator, operands) == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "operator, operands, value",
    [("-", ["1"], 1), ("-", ["1", "2"], -1), ("-", ["1", "2", "3"], -4),],
)
def test_subtract(operator, operands, value):
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
    assert handler.execute(operator, operands) == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "operator, operands, value",
    [("/", ["1"], 1), ("/", ["2", "2"], 1), ("/", ["12", "3", "2"], 2),],
)
def test_multiply(operator, operands, value):
    assert handler.execute(operator, operands) == value
