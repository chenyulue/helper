# conftest.py
import pytest

@pytest.fixture
def claims1(request):
    with open("tests/claims_set/claims1.txt", "r", encoding="utf-8") as f:
        claims = f.read()
    return claims

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")