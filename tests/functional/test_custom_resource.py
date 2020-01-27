import pytest

from src.cf.custom_resource import handler


@pytest.mark.functional
@pytest.mark.parametrize("operator, operands", [
    ("echo", ["this is a", "test"]),
    ("echo", ["this is a test"]),
    ("echo", [None]),
    ("echo", None),
    (["echo"], []),
    ("echo", ""),
    (["echo"], ""),
    ("echo", [])
])
def test_handler_echo(operator, operands):
    event = {
        "ResourceProperties": {
            "Operator": operator,
            "Operands": operands
        }
    }
    response = handler(event, {})

    assert int(response["statusCode"]) == 200


@pytest.mark.functional
@pytest.mark.parametrize("operator, operands", [
        ("", None),
        ("unknown", None)
])
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
@pytest.mark.parametrize("operator, operands", [
        ("", []),
])
def test_handler_missing_input(operator, operands):
    event = {
        "ResourceProperties": {
            "Operator": operator,
            "Operands": operands
        }
    }
    response = handler(event, {})

    assert int(response["statusCode"]) == 400
