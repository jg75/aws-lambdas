import pytest

from src.cf.network_calculator import handler


@pytest.mark.unit
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
    assert handler.execute(operator, operands) == value
