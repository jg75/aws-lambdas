import pytest

from src.cf.network_calculator import handler


@pytest.mark.unit
def test_handler_exists():
    assert handler
