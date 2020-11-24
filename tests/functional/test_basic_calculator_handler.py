"""Functional tests for the basic_calculator_handler."""
import pytest

from cf.basic_calculator import handler


def test_handler():
    """It should have a callable handler."""
    assert callable(handler)


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
    """It should return a status 200 on success."""
    event = {"ResourceProperties": {"Operator": operator, "Operands": operands}}
    response = handler(event, {})

    assert int(response["statusCode"]) == 200


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
    """It should return a status 400 on failure."""
    event = {"ResourceProperties": {"Operator": operator, "Operands": operands}}
    response = handler(event, {})

    assert int(response["statusCode"]) == 400
