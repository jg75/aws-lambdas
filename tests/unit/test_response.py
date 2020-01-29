"""Tests for src.cf.response."""
import requests
from unittest.mock import patch

import pytest

from src.cf import cfnresponse


@pytest.fixture
def status():
    """Get a sample status."""
    return "test-status"


@pytest.fixture
def data():
    """Get a sample response data dictionary."""
    return {"Value": "test-data-value"}


@pytest.mark.unit
def test_something(event, context, status, data):
    """Test that a response is being sent when a response url is present."""
    with patch("requests.put") as mock_put:
        cfnresponse.send(event, context, status, data)

    mock_put.assert_called_once()
