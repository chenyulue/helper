"""该模块用于解析权利要求文本"""

import re
import itertools
import functools

from collections.abc import Iterator

from ..core.BaseModel import BaseModel
from ..core.Types import Claim, RefPath


class ClaimModel(BaseModel):
    """ClaimModel类用于解析权利要求"""

    def __init__(self, data: str) -> None:
        """
        Parameters
        ----------
        data : str
            权利要求原始文本
        """
        super().__init__(data)

        self._claim_pattern = r"""
            ^(?P<number>\d+)\.\s*                                  # 权利要求编号
            (?P<leading>一种)?(?P<dep_exp>(?:根据|如)权?利?要?求?     # 从权的常规表述
            (?P<dep_num>.+?)所述的?)?                               # 从权的引用关系
            (?P<title>[^，]+)，                                     # 主题名称
            .+?(?:\n|$)                                            # 单行特征限定部分
            (?:^[^\d\n].+?(?:\n|$))*                               # 多行特征限定部分
            """

        self.claims = list(self.parse())
        self.get_reference_path = functools.lru_cache()(self._get_reference_path)

    def parse(self) -> Iterator[Claim]:
        claim = re.compile(self._claim_pattern, flags=re.X | re.M | re.S)

        for match in claim.finditer(self._data):
            number = int(match.group("number"))
            is_dependent = (
                match.group("leading") is None and match.group("dep_exp") is not None
            )
            title = match.group("title")
            content = match.group(0)
            start_pos = match.start()
            dependency, is_alternative = self._extract_dependency(
                match.group("dep_num"), number
            )

            yield Claim(
                number,
                dependency,
                is_dependent,
                is_alternative,
                title,
                content,
                start_pos,
            )

    def reset_model(self, data: str) -> None:
        self._data = data
        self.claims = list(self.parse())

    def _extract_dependency(
        self, dep_num: str | None, number: int
    ) -> tuple[list[int], bool | None]:
        """提取引用关系，同时判断是否为择一引用关系

        Parameters
        ----------
        dep_num : str | None
            权利要求中引用关系的表述，例如“1-5任一项”、“2或3”等
        number : int
            引用关系的权利要求编号，用于错误提示

        Returns
        -------
        tuple[list[int], bool | None]
            引用的权利要求编号列表；以及是否为择一引用，None表示相关权利要求是独立权利要求，无需判断

        Raises
        ------
        ValueError
            相关的引用关系表述不是已知的格式，无法解析
        """
        if dep_num is None:
            return [], None

        OR_PATTERN = r"(?:\d+[、，或])*\d+或\d+$"  # 修改此处的正则表达式时，注意同步修改下面各条件分支中的表达
        AND_PATTERN = r"((?:\d+[、，和及])*\d+[、，和及]\d+)(.*任意?一)?[^、，]*$"
        RANGE_PATTERN = r"(\d+)\s*[-~至到]\s*(\d+)(.*任意?一)?[^-~]*$"

        if dep_num.isdigit():
            return [int(dep_num)], True
        if re.match(OR_PATTERN, dep_num):
            return [int(i) for i in re.split("[、，或]", dep_num)], True
        if match := re.match(AND_PATTERN, dep_num):
            return [
                int(i) for i in re.split("[、，和及]", match.group(1))
            ], match.group(2) is not None
        if match := re.match(RANGE_PATTERN, dep_num):
            return (
                list(range(int(match.group(1)), int(match.group(2)) + 1)),
                match.group(3) is not None,
            )

        raise ValueError(
            f"权项{number}的编号引用撰写方式: “<b>{dep_num}</b>” 未被处理, <br>未能正确解析权利要求请反馈Bug"
        )

    def _get_reference_path(self, claim_number: int) -> list[RefPath]:
        """获取某项权利要求的完整引用路径列表，一个引用路径包括了从本权利要求至独立权利要求的
        引用路径上所有的权利要求编号，多项从属权利要求将包括多条引用路径。

        Parameters
        ----------
        claim_number : int
            权利要求编号

        Returns
        -------
        list[RefPath]
            某项权利要求所有的完整引用路径列表
        """
        # 如果该权利要求没有引用其他权利要求，直接返回编号
        if not self.claims[claim_number - 1].dependency:
            return [[claim_number]]

        # 否则，递归获取引用的权利要求的路径
        paths = []
        for referenced_claim in self.claims[claim_number - 1].dependency:
            # 递归获取被引用的权利要求的路径
            sub_paths = self._get_reference_path(referenced_claim)

            # 将当前权利要求加入到每个路径的前面
            for path in sub_paths:
                paths.append([claim_number] + path)

        return paths

    @staticmethod
    def flatten_paths(paths: list[RefPath]) -> list[int]:
        """将多个引用路径合并成一个单一列表，其中包括了所有引用路径上涉及的权利要求编号

        Parameters
        ----------
        paths : list[RefPath]
            完整的引用路径列表

        Returns
        -------
        list[int]
            所有引用路径上涉及的权利要求编号列表，删除了重复项
        """
        return sorted(set(itertools.chain(*paths)), reverse=True)
