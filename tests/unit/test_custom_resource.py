"""Tests for the CustomResourceHandler."""
from unittest.mock import patch, ANY

import pytest

from cf import cfnresponse
from cf.custom_resource import handler


@pytest.fixture
def echo_event(event):
    """Get a sample echo event."""
    event["ResourceProperties"] = {"Operator": "echo", "Operands": "test"}
    return event


def test_echo():
    """Test the default echo operation."""
    assert handler.execute("echo", "test") == "test"


def test_send_not_called(echo_event, context):
    """It should not call send if there is no response url in the event."""
    event = echo_event

    if "ResponseURL" in event:
        del event["ResponseURL"]

    with patch("cf.cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_not_called()


def test_send_called_with_success(echo_event, context):
    """It should call send if there is a response url in the event on success."""
    event = echo_event

    with patch("cf.cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_called_once_with(event, context, cfnresponse.SUCCESS, ANY)


def test_send_called_with_failed(echo_event, context):
    """It should call send if there is a response url in the event on failure."""
    event = echo_event
    event["ResourceProperties"] = {"Operator": "unknown", "Operands": "test"}

    with patch("cf.cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_called_once_with(event, context, cfnresponse.FAILED, ANY)
