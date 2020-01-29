"""Tests for the CustomResourceHandler base class."""
from unittest.mock import patch, ANY

import pytest

from src.cf import cfnresponse
from src.cf.custom_resource import handler


@pytest.fixture
def echo_event(event):
    """Get a sample echo event."""
    event["ResourceProperties"] = {"Operator": "echo", "Operands": "test"}
    return event

@pytest.mark.unit
def test_echo():
    """Test the default echo operation."""
    assert handler.execute("echo", "test") == "test"


@pytest.mark.unit
def test_send_not_called(echo_event, context):
    """It should not call send if there is no response url in the event."""
    event = echo_event

    if "ResponseURL" in event:
        del event["ResponseURL"]

    with patch("src.cf.cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_not_called()


@pytest.mark.unit
def test_send_called_with_success(echo_event, context):
    """It should call send if there is a response url in the event on success."""
    event = echo_event

    with patch("src.cf.cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_called_once_with(event, context, cfnresponse.SUCCESS, ANY)


@pytest.mark.unit
def test_send_called_with_failed(echo_event, context):
    """It should call send if there is a response url in the event on failure."""
    event = echo_event
    event["ResourceProperties"] = {"Operator": "unknown", "Operands": "test"}

    with patch("src.cf.cfnresponse.send") as mock_send:
        handler(event, context)

    mock_send.assert_called_once_with(event, context, cfnresponse.FAILED, ANY)
