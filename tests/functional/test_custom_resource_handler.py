import json

import pytest

from cf.custom_resource import handler


@pytest.mark.functional
def test_handler():
    assert callable(handler)


@pytest.mark.functional
@pytest.mark.parametrize(
    "operator, operands",
    [
        ("echo", ["this is a", "test"]),
        ("echo", ["this is a test"]),
        ("echo", [None]),
        (["echo"], []),
        ("echo", []),
        ("echo", "this is a test"),
        ("echo", ""),
        ("echo", None),
    ],
)
def test_handler_200(operator, operands):
    event = {"ResourceProperties": {"Operator": operator, "Operands": operands}}
    response = handler(event, {})
    body = json.loads(response["body"])

    if not isinstance(operands, (list)):
        operands = [operands]

    assert body["Value"] == operands
    assert int(response["statusCode"]) == 200


@pytest.mark.functional
@pytest.mark.parametrize("operator, operands", [("", None), ("unknown", None)])
def test_handler_400(operator, operands):
    event = {"ResourceProperties": {"Operator": operator, "Operands": operands}}
    response = handler(event, {})
    body = json.loads(response["body"])

    assert int(response["statusCode"]) == 400
    assert body["Exception"]
