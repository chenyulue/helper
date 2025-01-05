from abc import ABC, abstractmethod
from typing import Any

from .BaseModel import BaseModel
from .Types import CheckType

class BaseChecker(ABC):
    """各种形式缺陷检查的基类"""

    @abstractmethod
    def __init__(self, data: BaseModel) -> None:
        self._data = data
    @property
    @abstractmethod
    def name(self) -> CheckType:
        """检查器的类型，用于指示所检查的形式缺陷类型"""

    @abstractmethod
    def check(self, **kwargs) -> Any:
        """针对传递的数据进行特定缺陷的检查"""

    @abstractmethod
    def display(self, where: Any, result: Any, **kwargs: bool) -> None:
        """展示检查结果"""

    