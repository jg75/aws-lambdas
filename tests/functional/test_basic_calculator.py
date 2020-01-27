import pytest

from src.cf.basic_calculator import handler


@pytest.mark.functional
@pytest.mark.parametrize("operator, operands", [
    ("+", ["1"]),
    ("+", ["1", "1"]),
    ("+", ["1", "1", "1"]),
    ("-", ["1"]),
    ("-", ["1", "1"]),
    ("-", ["1", "1", "1"]),
    ("*", ["1"]),
    ("*", ["1", "1"]),
    ("*", ["1", "1", "1"]),
    ("/", ["1"]),
    ("/", ["1", "1"]),
    ("/", ["1", "1", "1"]),
    ("%", ["1"]),
    ("%", ["1", "1"]),
    ("%", ["1", "1", "1"])
])
def test_handler(operator, operands):
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
        ("/", ["1", "0"]),
        ("%", ["1", "0"]),
])
def test_handler_divide_by_zero(operator, operands):
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
        ("", ["1", "0"]),
        ("unknown", ["1", "0"]),
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
        ("+", []),
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
