"""Tests for src.cf.response."""
import requests
from requests.exceptions import RequestException
from unittest.mock import patch

import pytest

from cf import cfnresponse


@pytest.fixture
def bad_event(event):
    """Get a sample bad event that should cause an RequestException."""
    event["ResponseURL"] = "bad url"
    return event


@pytest.fixture
def status():
    """Get a sample status."""
    return "test-status"


@pytest.fixture
def data():
    """Get a sample response data dictionary."""
    return {"Value": "test-data-value"}


def test_cfnresponse(event, context, status, data):
    """It should send a response when a response url is present."""
    with patch("requests.put") as mock_put:
        cfnresponse.send(event, context, status, data)

    mock_put.assert_called_once()


def test_cfnresponse_exception(bad_event, context, status, data):
    """It should handle request exceptions."""
    event = bad_event

    with patch("requests.put") as mock_put:
        mock_put.side_effect = RequestException()

        cfnresponse.send(event, context, status, data)

    mock_put.assert_called_once()
