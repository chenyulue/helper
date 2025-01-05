from helper.checkers import CheckManager
from helper.core import BaseChecker

def test_check_manager():
    @CheckManager.register("claims")
    class A(BaseChecker):
        pass
    
    assert A in CheckManager.checkers["claims"]

    @CheckManager.register(kind="description")
    class B(BaseChecker):
        pass

    assert B in CheckManager.checkers["description"]
