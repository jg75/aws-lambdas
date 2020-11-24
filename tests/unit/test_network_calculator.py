"""Tests for the NetworkCalculatorHandler."""
import pytest

from cf.network_calculator import handler


@pytest.mark.parametrize(
    "operator, operands, value",
    [
        ("SubnetSize", ["24", "1"], 8),
        ("SubnetSize", ["24", "2"], 7),
        ("SubnetSize", ["24", "3"], 7),
        ("SubnetSize", ["24", "4"], 6),
        ("SubnetSize", ["24", "5"], 6),
        ("SubnetSize", ["24", "6"], 6),
        ("SubnetSize", ["24", "7"], 6),
        ("SubnetSize", ["24", "8"], 5),
    ],
)
def test_subnet_size(operator, operands, value):
    """It should be able to calculate subnet size."""
    assert handler.execute(operator, operands) == value
