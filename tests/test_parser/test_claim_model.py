import pytest

from helper.parser import ClaimModel

CLAIM_1 = """1. 一种半导体器件，其包括MOS晶体管。
2. 根据权利要求1所述的器件，其进一步包括一个栅极。
3. 根据权利要求2所述的器件，所述栅极由金属构成。
"""

CLAIM_2 = """1. 
一种半导体器件，其包括MOS晶体管。
2. 
根据权利要求1所述的器件，其进一步包括一个栅极。
3. 
根据权利要求2所述的器件，所述栅极由金属构成。
"""

CLAIM_3 = """1. 一种半导体器件，其包括MOS晶体管;
所述MOS晶体管包括源极和漏极；
所述漏极接电源正极。
2. 根据权利要求1所述的器件，其进一步包括一个栅极。
3. 根据权利要求2所述的器件，所述栅极由金属构成。"""

CLAIM_4 = """1. 一种半导体器件，其包括MOS晶体管。
2. 根据权利要求1所述的器件，其进一步包括一个栅极。
3. 根据权利要求1或2所述的器件，其进一步包括源极和漏极。
4. 如权利要求1-3中任一所述的器件，所述晶体管的制备材料为硅。
5. 一种根据权利要求1-4所述的半导体器件的制备方法，其采用外延工艺。
6. 如权利要求5所述的制备方法，其采用CVD工艺。
7. 根据权利要求5、6所述的制备方法，所述CVD工艺采用硅源。

"""

TITLES = ["半导体器件", "器件", "器件"]
DEPS = [[], [1], [2]]
IS_ALTERNATIVE = [None, True, True]


@pytest.mark.parametrize(
    "claim, pos",
    [
        (CLAIM_1, [0, 22, 50]),
        (CLAIM_2, [0, 23, 52]),
        (CLAIM_3, [0, 50, 78]),
    ],
)
def test_claim_model_parse(claim, pos):
    model = ClaimModel(claim)
    results = list(model.parse())

    for i, result in enumerate(results):
        assert result.number == i + 1
        assert result.title == TITLES[i]
        assert result.dependency == DEPS[i]
        assert result.is_alternative == IS_ALTERNATIVE[i]
        assert result.start_pos == pos[i]

    assert "".join(result.content for result in results) == claim


def test_claim_model_parse_complex_claims():
    model = ClaimModel(CLAIM_4)
    results = list(model.parse())

    assert len(results) == 7

    deps = [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [5], [5, 6]]
    is_alternative = [None, True, True, True, False, True, False]
    is_dependent = [False, True, True, True, False, True, True]
    title = [
        "半导体器件",
        "器件",
        "器件",
        "器件",
        "半导体器件的制备方法",
        "制备方法",
        "制备方法",
    ]
    start_pos = [0, 22, 50, 81, 115, 152, 179]
    for i, result in enumerate(results):
        assert result.number == i + 1
        assert result.dependency == deps[i]
        assert result.is_alternative is is_alternative[i]
        assert result.is_dependent is is_dependent[i]
        assert result.title == title[i]
        assert result.start_pos == start_pos[i]

    assert "".join(result.content for result in results) == CLAIM_4[:-1]


@pytest.mark.parametrize(
    "dep_num, deps, is_alternative",
    [
        (None, [], None),
        ("12", [12], True),
        ("2或14", [2, 14], True),
        ("2、3或14", [2, 3, 14], True),
        ("4和6任一项", [4, 6], True),
        ("4和6", [4, 6], False),
        ("4、6和12任意一项", [4, 6, 12], True),
        ("4、6和12", [4, 6, 12], False),
        ("4-7任一项", [4, 5, 6, 7], True),
        ("4-7中任意一项", [4, 5, 6, 7], True),
        ("4-7", [4, 5, 6, 7], False),
        ("3至9", [3, 4, 5, 6, 7, 8, 9], False),
        ("3、6、9", [3, 6, 9], False),
    ],
)
def test_claim_model_extract_dependency(dep_num, deps, is_alternative):
    model = ClaimModel("")
    a, b = model._extract_dependency(dep_num, 1)
    assert a == deps
    assert b == is_alternative


def test_claim_model_extract_dependency_error():
    model = ClaimModel("")

    with pytest.raises(ValueError, match=r"权项1.+1-2-3.+"):
        model._extract_dependency("1-2-3", 12)


def test_claim_model_reset_model():
    model = ClaimModel(CLAIM_1)
    assert model._data == CLAIM_1

    model.reset_model(CLAIM_2)
    assert model._data == CLAIM_2


def test_claim_model_get_reference_path():
    model = ClaimModel(CLAIM_4)
    assert model.get_reference_path(1) == [[1]]
    assert model.get_reference_path(2) == [[2, 1]]
    assert model.get_reference_path(3) == [[3, 1], [3, 2, 1]]
    assert model.get_reference_path(4) == [[4, 1], [4, 2, 1], [4, 3, 1], [4, 3, 2, 1]]
    assert model.get_reference_path(5) == [
        [5, 1],
        [5, 2, 1],
        [5, 3, 1],
        [5, 3, 2, 1],
        [5, 4, 1],
        [5, 4, 2, 1],
        [5, 4, 3, 1],
        [5, 4, 3, 2, 1],
    ]
    assert model.get_reference_path(6) == [
        [6, 5, 1],
        [6, 5, 2, 1],
        [6, 5, 3, 1],
        [6, 5, 3, 2, 1],
        [6, 5, 4, 1],
        [6, 5, 4, 2, 1],
        [6, 5, 4, 3, 1],
        [6, 5, 4, 3, 2, 1],
    ]
    assert model.get_reference_path(7) == [
        [7, 5, 1],
        [7, 5, 2, 1],
        [7, 5, 3, 1],
        [7, 5, 3, 2, 1],
        [7, 5, 4, 1],
        [7, 5, 4, 2, 1],
        [7, 5, 4, 3, 1],
        [7, 5, 4, 3, 2, 1],
        [7, 6, 5, 1],
        [7, 6, 5, 2, 1],
        [7, 6, 5, 3, 1],
        [7, 6, 5, 3, 2, 1],
        [7, 6, 5, 4, 1],
        [7, 6, 5, 4, 2, 1],
        [7, 6, 5, 4, 3, 1],
        [7, 6, 5, 4, 3, 2, 1],
    ]


def test_claim_model_flatten_paths():
    model = ClaimModel("")
    assert model.flatten_paths([[5, 4, 3, 1], [5, 2, 1]]) == [5, 4, 3, 2, 1]
