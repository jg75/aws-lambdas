import pytest

from src.cf.network_calculator import handler


@pytest.mark.functional
def test_handler_ipv4_subnet_size():
    def run(netmask_bits, subnets):
        event = {
            "ResourceProperties": {
                "Operator": "SubnetSize",
                "Operands": [str(netmask_bits), str(subnets)]
            }
        }
        response = handler(event, {})

        assert int(response["statusCode"]) == 200

    for netmask_bits in range(16, 29):
        for subnets in range(1, 9):
            run(netmask_bits, subnets)


@pytest.mark.functional
@pytest.mark.parametrize("operator, operands", [("", None), ("unknown", None)])
def test_handler_unknown(operator, operands):
    event = {
        "ResourceProperties": {
            "Operator": operator,
            "Operands": operands
        }
    }
    response = handler(event, {})

    assert int(response["statusCode"]) == 400


@pytest.mark.functional
@pytest.mark.parametrize("operator, operands", [("", []), ("", ["one"])])
def test_handler_missing_input(operator, operands):
    event = {
        "ResourceProperties": {
            "Operator": operator,
            "Operands": operands
        }
    }
    response = handler(event, {})

    assert int(response["statusCode"]) == 400
