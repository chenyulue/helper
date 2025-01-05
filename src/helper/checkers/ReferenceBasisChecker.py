"""该模块定义了权利要求中引用基础的检查器类，用于检查引用的特征在之前的描述中是否被清晰地定义或提及。"""

import re

from PyQt5.QtWidgets import QTextBrowser

from ..core import BaseChecker
from ..parser import ClaimModel
from ..core.Types import Claim, RefBasis, ContextInfo, CheckType

from .CheckManager import CheckManager


@CheckManager.register("claim")
class ReferenceBasisChecker(BaseChecker):
    """检查权利要求中引用的基础是否在之前的描述中清晰定义或提及"""

    def __init__(self, data: ClaimModel) -> None:
        self._data = data

        self.has_basis: set[int] = set()  # 保存确认过的具有引用基础的权利要求编号
        self.lack_basis: set[int] = set()  # 保存确认过的缺乏引用基础的权利要求编号

    @property
    def name(self) -> CheckType:
        return CheckType.LackOfReferenceBasis

    def update_has_basis(self, value: int, add: bool = True) -> None:
        if add:
            self.has_basis.add(value)
            if value in self.lack_basis:
                self.lack_basis.remove(value)
        else:
            self.has_basis.remove(value)

    def update_lack_basis(self, value: int, add: bool = True) -> None:
        if add:
            self.lack_basis.add(value)
            if value in self.has_basis:
                self.has_basis.remove(value)
        else:
            self.lack_basis.remove(value)

    def check(self, **kwargs: int) -> dict[int, dict[int, RefBasis]]:
        """该函数根据特定的截词长度，检查权利要求书中所有缺乏引用基础的缺陷，其中，key是权利要求编号，
        value是针对每个权利要求的引用缺陷dict。在该引用缺陷dict中，其key值为该权利要求中存在*所述*
        等表述的技术特征在原始权利要求文本中的位置（用于后续在原始权利要求中定位并格式化相关特征表述），
        而value值是一个RefBais对象，其记录缺乏引用基础的相关信息。

        Parameters
        ----------
        length : int
            技术术语的截词长度

        Returns
        -------
        Iterator[tuple[int, dict[int, RefBasis]]]
            返回一个迭代器，其中，每个元素是一个元组，元组的第一个元素是权利要求编号，第二个元素是该权利要求中所有缺乏引用基础的
            技术特征的检查结果字典，其中该字典的key值是该技术特征在原始权利要求文本中的位置
        """
        if "length" not in kwargs:
            raise TypeError(
                f"check() from `{self.__class__.__name__}` needs a keyword argument 'length'"
            )

        length = kwargs["length"]
        result = {}

        for claim in self._data.claims:
            result[claim.number] = self._check_reference_basis(claim, length)

        return result

    def display(
        self,
        where: QTextBrowser,
        result: dict[int, dict[int, RefBasis]],
        **kwargs: bool,
    ) -> None:
        """该函数用于在GUI界面上显示检查结果

        Parameters
        ----------
        where : QTextBrowser
            检查结果显示的位置
        result : dict[int, dict[int, RefBasis]]
            检查结果
        """
        if kwargs.get("show_claim", True):
            where.display_reference_basis(
                result, self.has_basis, self.lack_basis, self.get_all_reference_paths()
            )

    def get_all_reference_paths(self) -> dict[int, list[int]]:
        """获取所有权利要求的引用路径

        Parameters
        ----------
        None

        Returns
        -------
        dict[int, list[int]]
            key是权利要求编号，value是该权利要求所有引用路径上包含权利要求编号（该权利要求
            的编号除外）
        """
        reference_path: dict[int, list[int]] = {}
        for i, _ in enumerate(self._data.claims):
            paths = self._data.flatten_paths(self._data.get_reference_path(i + 1))
            reference_path[i + 1] = paths[1:]
        return reference_path

    def _check_reference_basis(self, claim: Claim, length: int) -> dict[int, RefBasis]:
        """检查某一项权利要求是否存在缺乏引用基础的缺陷

        Parameters
        ----------
        claim : Claim
            待查权利要求
        length : int
            待查术语的截词长度

        Returns
        -------
        dict[int, RefBasis]
            key是权利要求中存在*所述*等表述的技术特征在原始权利要求文本中的位置（用于后续在原始
            权利要求中定位并格式化相关特征表述），而value值是一个RefBais
        """
        ref_basis: dict[int, RefBasis] = {}
        for term, info in self._get_terminology(claim, length).items():
            pos = claim.start_pos + info.pos
            result = self._reference_has_basis(claim, term, info.pos)

            ref_basis[pos] = RefBasis(pos, term, info.context, result)

        return ref_basis

    def _get_terminology(self, claim: Claim, length: int) -> dict[str, ContextInfo]:
        """获取特定权利要求中所有首次引用的技术特征

        Parameters
        ----------
        claim : Claim
            待查的权利要求
        length : int
            技术特征的截词长度

        Returns
        -------
        dict[str, tuple[int, str]]
            key是获取的技术特征文本，value则包括该技术特征在权利要求中的位置、以及该技术特征在权利要求
            中的上下文环境，该上下文环境指的是从“所述”等引导词开始直至下一个“所述”等引导词或下一个标点
            符号为止这一范围内的文本
        """
        preceding_words = "所述的?|上述的?|前述的?|该些?"
        PATTERN = (
            "(?:"
            f"{preceding_words})"
            "([^，。；,;]{1,"
            f"{length}"
            "}).*?(?=[，。；,;、]|"
            f"{preceding_words})"
        )
        pattern = re.compile(PATTERN)

        terms = {}
        for match in pattern.finditer(claim.content):
            terms.setdefault(match.group(1), ContextInfo(match.start(), match.group()))

        return terms

    def _reference_has_basis(
        self, claim: Claim, terminology: str, pos: int
    ) -> bool | list[int]:
        """检查某一项权利要求中某个技术特征是否存在引用基础

        Parameters
        ----------
        claim : Claim
            待检查的权利要求
        terminology : str
            待检查的技术特征
        pos : int
            待检查的技术特征在该权利要求中的位置，用于限定在本权利要求中检查是否存在引用基础
            的查找范围

        Returns
        -------
        bool | list[int]
            在所有引用路径上都存在该术语则返回True，在所有路径上都不存在该术语则返回False；
            如果只在部分引用路径上存在该术语，则返回引用路径上存在该技术术语的权利要求编号列表
        """
        pattern = re.compile(terminology)

        # 检查当前权利要求中在该技术术语之前的文本中是否定义了该术语
        if pattern.search(claim.content, 0, pos):
            return True
        # 检查其引用的权利要求中是否定义了该术语
        else:
            return self._terminology_exists_in_references(pattern, claim.number)

    def _terminology_exists_in_references(
        self,
        pattern: re.Pattern,
        claim_number: int,
    ) -> bool | list[int]:
        """检查某一项权利要求中相关技术特征在引用路径上的在前权利要求中是否存在定义

        Parameters
        ----------
        pattern : re.Pattern
            技术特征的正则表达式模式
        claim_number : int
            检查的权利要求编号

        Returns
        -------
        bool | list[int]
            在所有引用路径上都存在该术语则返回True，在所有路径上都不存在该术语则返回False；
            如果只在部分引用路径上存在该术语，则返回引用路径上存在该技术术语的权利要求编号列表
        """
        ref_paths = self._data.get_reference_path(claim_number)

        existed_refs = []
        for ref_number in self._data.flatten_paths(ref_paths)[1:]:
            ref_claim = self._data.claims[ref_number - 1]
            if pattern.search(ref_claim.content):
                # 如果存在该术语的权利要求编号在所有的引用路径上，则直接返回True
                if all(ref_number in paths for paths in ref_paths):
                    return True
                # 收集存在该术语的部分引用路径
                else:
                    existed_refs.append(ref_number)

        # 若existed_refs为空列表，则表明所有引用路径上涉及的所有在前权利要求中都不存在该技术术语
        return existed_refs if existed_refs else False
