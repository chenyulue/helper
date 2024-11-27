# conftest.py
import pytest

@pytest.fixture
def claims1():
    with open("tests/claims_set/claims1.txt", "r", encoding="utf-8") as f:
        claims = f.read()
    return claims