from unittest.mock import patch, ANY

import cfnresponse
import pytest

from src.cf.custom_resource import handler


@pytest.mark.unit
def test_echo():
    assert handler.execute("echo", "test") == "test"


@pytest.mark.unit
def test_send_not_called():
    event = {"ResourceProperties": {"Operator": "echo", "Operands": "test"}}
    context = {}

    with patch("cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_not_called()


@pytest.mark.unit
def test_send_called_with_success():
    event = {
        "ResponseURL": "test",
        "ResourceProperties": {"Operator": "echo", "Operands": "test"},
    }
    context = {}

    with patch("cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_called_once_with(event, context, cfnresponse.SUCCESS, ANY)


@pytest.mark.unit
def test_send_called_with_failed():
    event = {"ResponseURL": "test"}
    context = {}

    with patch("cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_called_once_with(event, context, cfnresponse.FAILED, ANY)
