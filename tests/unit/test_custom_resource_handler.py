import pytest

from src.cf.custom_resource import handler


@pytest.mark.unit
def test_handler_exists():
    assert handler
