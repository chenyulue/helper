"""该模块定义了helper所使用的一些数据类型"""

from dataclasses import dataclass


@dataclass
class Claim:
    """Claim类，作为权利要求文本解析生成的结果。

    Parameters
    -------
    number: int
        权利要求编号
    dependency: list[int]
        引用的权利要求编号
    is_dependent: bool
        独立权利要求为False，从属权利要求为True
    is_alternative: bool | None
        从属权利要求中，择一引用为True，非择一引用为False；对于独立权利要求，其值为None
    title: str
        权利要求的主题名称，其中独立权利要求为第一个逗号之前整个主题名称部分，而从属权利要求则为
        “所述”等表述后的主题部分
    content: str
        该项权利要求的原始文本
    start_pos: int
        该项权利要求在原始权利要求文本中位置
    """

    number: int
    dependency: list[int]
    is_dependent: bool
    is_alternative: bool | None
    title: str
    content: str
    start_pos: int


@dataclass
class RefBasis:
    """缺乏引用基础的技术特征的相关信息

    Parameters
    ----------
    position : int
        缺乏引用基础的相关特征表述在原始权利要求中的位置，记录“所述”开始的位置
    term: str
        缺乏引用基础的相关特征术语，即“所述”之后的特征
    context: str
        缺乏引用基础的相关特征的上下文文本，从该“所述”等引用词开始直至下一个标点符号或者下一个“所述”等引用词的文本范围
    hasbasis_checked: bool | list[int]
        程序检查的缺乏引用基础问题的结果，所有引用路径都有引用基础则为True，所有引用路径都没有引用基础则为False，
        部分引用路径有引用基础，则记录这些部分引用路径。
    """

    position: int
    term: str
    context: str
    hasbasis_confirmed: bool | None
    hasbasis_checked: bool | list[int]


class RefBasisConfirmed:
    """缺乏引用基础检查结果的确认类"""

    __slots__ = ("has_basis", "lack_basis")

    def __init__(
        self, has_basis: set[int] | None = None, lack_basis: set[int] | None = None
    ) -> None:
        self.has_basis = has_basis or set()
        self.lack_basis = lack_basis or set()

    def __str__(self):
        return f"has basis: {self.has_basis}, lack basis: {self.lack_basis}"
