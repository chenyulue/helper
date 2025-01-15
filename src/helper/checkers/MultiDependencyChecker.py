from PyQt5.QtWidgets import QTextBrowser

from ..core import BaseChecker
from ..parser import ClaimModel
from ..core.Types import Claim, CheckType

from .CheckManager import CheckManager


@CheckManager.register("claim")
class MultiDependencyChecker(BaseChecker):
    """检查权利要求中是否存在多引多的缺陷"""

    def __init__(self, data: ClaimModel) -> None:
        self._data = data

        self.results: dict[int, list[int]] | None = None

    @property
    def name(self) -> CheckType:
        return CheckType.MultiDependency

    def check(self, **kwargs) -> dict[int, list[int]]:
        """检查多引多缺陷，检查结果为一个dict，其中key为存在多引多缺陷的权项，value为所引用的
        多项从属权利要求。
        """
        if self.results is None:
            self.results = {
                claim.number: result[1]
                for claim in self._data.claims
                if (result := self._check_multiple_dependencies(claim))[0]
            }
        return self.results

    def display(
        self,
        where: QTextBrowser,
        result: dict[int, list[int]],
        **kwargs: bool,
    ) -> None:
        """该函数用于在GUI界面上显示检查结果

        Parameters
        ----------
        where : QTextBrowser
            检查结果显示的位置
        result : dict[int, list[int]]
            检查结果
        """
        if kwargs.get("show_claim", True):
            where.display_multiple_dependencies(result)

    def _check_multiple_dependencies(self, claim: Claim) -> tuple[bool, list[int]]:
        """检查某项权利要求是否存在多引多的缺陷"""
        if len(claim.dependency) > 1:
            multiple_dependencies = [
                ref
                for ref in claim.dependency
                if len(self._data.claims[ref - 1].dependency) > 1
            ]
            return len(multiple_dependencies) > 0, multiple_dependencies
        return False, []
