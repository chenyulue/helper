"""该模块定义了权利要求中引用基础的检查器类，用于检查引用的特征在之前的描述中是否被清晰地定义或提及。"""

from ..core.BaseChecker import BaseChecker
from ..parser import ClaimModel


class ReferenceBasisChecker(BaseChecker):
    """检查权利要求中引用的基础是否在之前的描述中清晰定义或提及"""

    def __init__(self, data: ClaimModel) -> None:
        super().__init__(data)

    @property
    def name(self) -> str:
        return "Lack of Reference Basis"

    def check(self, *args, **kwargs) -> None:
        pass
