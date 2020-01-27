import pytest

from src.cf.basic_calculator import handler


@pytest.mark.unit
def test_handler_exists():
    assert handler
