import re
import pytest
from helper.models import ClaimModel, Claim


def test_claim_model(claims1):
    claim_model = ClaimModel(claims1)
    assert len(claim_model.claims) == 12

    for claim in claim_model.claims:
        if claim.number < 10:
            assert claims1[claim.start_pos] == str(claim.number)
        else:
            assert claims1[claim.start_pos : claim.start_pos + 2] == str(claim.number)

    assert claim_model.claims[6].dependency == [4, 6]
    assert claim_model.claims[1].dependency == [1]
    assert claim_model.claims[6].title == "场效应晶体管"
    assert claim_model.claims[0].dependency == []
    assert claim_model.claims[0].is_alternative is None
    assert claim_model.claims[9].dependency == [8, 9]
    assert claim_model.claims[9].is_alternative is False
    assert claim_model.claims[11].dependency == [3, 4, 5, 6, 7, 8, 9, 10]
    assert claim_model.claims[11].is_alternative is True


@pytest.mark.parametrize(
    "deps,dependency,is_alternative",
    [
        [None, [], None],
        ("4", [4], True),
        ("4或6", [4, 6], True),
        ("4、6或8", [4, 6, 8], True),
        ("5-10任一项", [5, 6, 7, 8, 9, 10], True),
        ("5-10", [5, 6, 7, 8, 9, 10], False),
        ("5、6，7和8", [5, 6, 7, 8], False),
        ("5、6、7和8任一项", [5, 6, 7, 8], True),
    ],
)
def test_parse_dependency(deps, dependency, is_alternative):
    claim_model = ClaimModel("")
    assert claim_model._parse_dependency(deps) == (dependency, is_alternative)


def test_parse_dependency_errors():
    claim_model = ClaimModel("")
    with pytest.raises(ValueError) as e:
        claim_model._parse_dependency("5 AND 6")
    assert "权利要求引用撰写方式:`5 AND 6`未被处理, 请反馈Bug" in str(e.value)


def test_get_reference_path():
    claim_model = ClaimModel("")
    claims_references = {
        1: [],  # 权利要求1是独立权利要求，不引用任何其他权利要求
        2: [1],  # 权利要求2引用权利要求1
        3: [1],  # 权利要求3引用权利要求1
        4: [2, 3],  # 权利要求4同时引用权利要求2和权利要求3
        5: [4],  # 权利要求5引用权利要求4
        6: [2],  # 权利要求6引用权利要求2
        7: [4, 5],  # 权利要求7同时引用权利要求4和权利要求5
        8: [7],  # 权利要求8引用权利要求7
    }
    claims = tuple([Claim(i, j, False, False, "", f"{i}+{j}", 0) for i, j in claims_references.items()])
    assert claim_model._get_reference_path(1, claims) == [[1]]
    assert claim_model._get_reference_path(2, claims) == [[2, 1]]
    assert claim_model._get_reference_path(3, claims) == [[3, 1]]
    assert claim_model._get_reference_path(4, claims) == [[4, 2, 1], [4, 3, 1]]
    assert claim_model._get_reference_path(5, claims) == [[5, 4, 2, 1], [5, 4, 3, 1]]
    assert claim_model._get_reference_path(6, claims) == [[6, 2, 1]]
    assert claim_model._get_reference_path(7, claims) == [[7, 4, 2, 1], [7, 4, 3, 1], [7, 5, 4, 2, 1], [7, 5, 4, 3, 1]]
    assert claim_model._get_reference_path(8, claims) == [[8, 7, 4, 2, 1], [8, 7, 4, 3, 1], [8, 7, 5, 4, 2, 1], [8, 7, 5, 4, 3, 1]]

def test_flattern_path():
    claim_model = ClaimModel("")
    paths = [
        [1, 2, 3],
        [1, 2, 4],
        [1, 3, 4],
        [2, 3, 4],
    ]
    assert claim_model._flatten_paths(paths) == [4,3,2,1]

@pytest.mark.parametrize("claims1, number, term, expected", [
    ("", 1, "第一介质区", True),
    ("", 12, "电流引导层", [10, 9, 5, 4, 3]),
    ("", 8, "纳米线", False),
    ("", 7, "电场屏蔽区", True)
], indirect=["claims1"])
def test_reference_has_basis(claims1, number, term, expected):
    claim_model = ClaimModel(claims1)
    match = re.search(f"所述({term})", claim_model.claims[number - 1].content)
    if match:
        start_pos = match.start()
        assert claim_model._reference_has_basis(claim_model.claims[number - 1], term, start_pos, claim_model.claims) == expected

def test_get_terminology(claims1):
    claim_model = ClaimModel(claims1)
    result = claim_model._get_terminology(claim_model.claims[11], 3)
    assert result == {"电流引": (32,"所述电流引导层（9）的掺杂浓度大于"), "外延层": (49,"所述外延层"), "场效应": (16,"所述的场效应晶体管")}

    result = claim_model._get_terminology(claim_model.claims[11], 5)
    assert result == {"电流引导层": (32,"所述电流引导层（9）的掺杂浓度大于"), "外延层": (49,"所述外延层"), "场效应晶体": (16,"所述的场效应晶体管")}

    result = claim_model._get_terminology(claim_model.claims[7], 3)
    assert result["纳米线"] == (43,"所述纳米线第二掺杂类型的源区（16）")
    
    
