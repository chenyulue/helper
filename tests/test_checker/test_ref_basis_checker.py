import pytest

from helper.checkers import ReferenceBasisChecker
from helper.parser import ClaimModel
from helper.core.Types import Claim, ContextInfo

CLAIM_1 = """1. 一种智能手表，其特征在于，包括：
    一个表带，用于固定在用户手腕上；
    一个显示屏，用于显示时间和通知信息；
    一个内置传感器模块，用于监测用户的心率和运动数据；
    其中，所述显示屏与所述内置传感器模块通过无线通信连接，以实现数据的实时显示和分析。

2. 根据权利要求1所述的智能手表，其特征在于，所述内置传感器模块包括：
    一个心率传感器，用于检测用户的心率；
    一个加速度计，用于检测用户的运动状态；
    其中，心率传感器与加速度计通过内置电路板连接，以实现数据的集成处理。

3. 根据权利要求1或2所述的智能手表，其特征在于，所述显示屏具有触控功能，以实现用户通过触摸进行操作和设置。

4. 一种使用根据权利要求1至3中任一项所述的智能手表的方法，其特征在于，包括以下步骤：
    步骤1：将智能手表固定在用户手腕上；
    步骤2：启动手表的监测功能，开始记录心率和运动数据；
    步骤3：通过触控显示屏查看实时数据和历史记录；
    步骤4：根据监测结果调整运动计划或健康习惯。
"""

@pytest.fixture
def checker():
    return ReferenceBasisChecker(ClaimModel(CLAIM_1))

def test_ref_checker_update_lack_basis(checker):
    assert checker.lack_basis == set()
    checker.update_lack_basis(3)
    assert checker.lack_basis == {3}
    checker.update_lack_basis(4)
    assert checker.lack_basis == {3, 4}


def test_ref_checker_get_terminology(checker):
    content = "3. 根据权利要求1所述的器件，所述源极位于所述器件内部，所述源极由金属制成。"
    claim = Claim(1, [], True, None, "", content, 1)

    result = checker._get_terminology(claim, 2)
    assert result == {
        "器件": ContextInfo(10, "所述的器件"),
        "源极": ContextInfo(16, "所述源极位于")
    }

    result = checker._get_terminology(claim, 3)
    assert result == {
        "器件": ContextInfo(10, "所述的器件"),
        "源极位": ContextInfo(16, "所述源极位于"),
        "器件内": ContextInfo(22, "所述器件内部"),
        "源极由": ContextInfo(29, "所述源极由金属制成"),
    }

