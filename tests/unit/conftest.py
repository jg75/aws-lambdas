"""Conftest."""
import pytest


@pytest.fixture
def event():
    """Get a sample lambda event."""
    return {
        "ResponseURL": "https://test-url.example.com",
        "StackId": "test-stack-id",
        "RequestId": "test-request-id",
        "LogicalResourceId": "test-logical-id",
    }


@pytest.fixture
def context():
    """Get a sample lambda context."""
    class Context:
        log_stream_name = "test-log-stream"

    return Context()
