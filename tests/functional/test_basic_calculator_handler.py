import pytest

from src.cf.basic_calculator import handler


@pytest.mark.functional
def test_handler():
    assert callable(handler)


@pytest.mark.functional
@pytest.mark.parametrize(
    "operator, operands",
    [
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
        ("%", ["1", "1", "1"]),
    ],
)
def test_handler_200(operator, operands):
    event = {"ResourceProperties": {"Operator": operator, "Operands": operands}}
    response = handler(event, {})

    assert int(response["statusCode"]) == 200


@pytest.mark.functional
@pytest.mark.parametrize(
    "operator, operands",
    [
        ("/", ["1", "0"]),
        ("%", ["1", "0"]),
        ("", ["1", "0"]),
        ("unknown", ["1", "0"]),
        ("+", []),
    ],
)
def test_handler_400(operator, operands):
    event = {"ResourceProperties": {"Operator": operator, "Operands": operands}}
    response = handler(event, {})

    assert int(response["statusCode"]) == 400
