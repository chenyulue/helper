import pytest
from helper.models import ClaimModel

def test_claim_model(claims1):
    claim_model = ClaimModel(claims1)
    assert len(claim_model.claims) == 12

    for claim in claim_model.claims:
        if claim.number < 10:
            assert claims1[claim.start_pos] == str(claim.number)
        else:
            assert claims1[claim.start_pos : claim.start_pos+2] == str(claim.number)

    assert claim_model.claims[6].dependency == [4, 6]
    assert claim_model.claims[1].dependency == [1]
    assert claim_model.claims[6].title == "场效应晶体管"
    assert claim_model.claims[0].dependency == []
    assert claim_model.claims[0].is_alternative is None
    assert claim_model.claims[9].dependency == [8, 9]
    assert claim_model.claims[9].is_alternative is False
    assert claim_model.claims[11].dependency == [3, 4, 5, 6, 7, 8, 9, 10]
    assert claim_model.claims[11].is_alternative is True

@pytest.mark.parametrize("deps,dependency,is_alternative", [
    [None, [], None],
    ("4", [4], True),
    ("4或6", [4, 6], True),
    ("4、6或8", [4, 6, 8], True),
    ("5-10任一项", [5, 6, 7, 8, 9, 10], True),
    ("5-10", [5, 6, 7, 8, 9, 10], False),
    ("5、6，7和8", [5, 6, 7, 8], False),
    ("5、6、7和8任一项", [5, 6, 7, 8], True),
])
def test_parse_dependency(deps, dependency, is_alternative):
    claim_model = ClaimModel("")
    assert claim_model._parse_dependency(deps) == (dependency, is_alternative)

def test_parse_dependency_errors():
    claim_model = ClaimModel("")
    with pytest.raises(ValueError) as e:
        claim_model._parse_dependency("5 AND 6")
    assert "权利要求引用撰写方式:`5 AND 6`未被处理, 请反馈Bug" in str(e.value)