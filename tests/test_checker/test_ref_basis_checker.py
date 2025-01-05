
from helper.checkers import ReferenceBasisChecker
from helper.parser import ClaimModel

def test_ref_checker_update_lack_basis():
    checker = ReferenceBasisChecker(ClaimModel(""))
    assert checker.lack_basis == set()
    checker.update_lack_basis(3)
    assert checker.lack_basis == {3}
    checker.update_lack_basis(4)
    assert checker.lack_basis == {3, 4}

