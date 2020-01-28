import pytest

from src.cf.network_calculator import handler


@pytest.mark.functional
def test_handler():
    assert callable(handler)


@pytest.mark.functional
def test_handler_200():
    def run(netmask_bits, subnets):
        event = {
            "ResourceProperties": {
                "Operator": "SubnetSize",
                "Operands": [str(netmask_bits), str(subnets)],
            }
        }
        response = handler(event, {})

        assert int(response["statusCode"]) == 200

    for netmask_bits in range(16, 29):
        for subnets in range(1, 9):
            run(netmask_bits, subnets)


@pytest.mark.functional
@pytest.mark.parametrize(
    "operator, operands",
    [("", None), ("unknown", None), ("SubnetSize", []), ("SubnetSize", ["one"])],
)
def test_handler_400(operator, operands):
    event = {"ResourceProperties": {"Operator": operator, "Operands": operands}}
    response = handler(event, {})

    assert int(response["statusCode"]) == 400
