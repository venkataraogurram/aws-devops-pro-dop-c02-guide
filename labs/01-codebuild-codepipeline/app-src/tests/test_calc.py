import pytest
from app.calc import add, discount


def test_add():
    assert add(2, 3) == 5


def test_discount():
    assert discount(200, 10) == 180.0


def test_discount_rejects_bad_percent():
    with pytest.raises(ValueError):
        discount(100, 150)
