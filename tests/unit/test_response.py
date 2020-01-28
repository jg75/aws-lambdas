import requests
from unittest.mock import patch

import pytest

from src.cf.response import CloudFormationResponse, SUCCESS, FAILED


@pytest.fixture
def event():
    return {
        "ResponseURL": "https://test-url.example.com",
        "StackId": "test-stack-id",
        "RequestId": "test-request-id",
        "LogicalResourceId": "test-logical-id",
    }


@pytest.fixture
def context():
    class Context:
        log_stream_name = "test-log-stream"

    return Context()


@pytest.fixture
def status():
    return "test-status"


@pytest.fixture
def data():
    return {"Value": "test-data-value"}


@pytest.mark.unit
def test_something(event, context, status, data):
    response = CloudFormationResponse()

    with patch("requests.put") as mock_put:
        response.send(event, context, status, data)

    mock_put.assert_called_once()
