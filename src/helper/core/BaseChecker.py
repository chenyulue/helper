from abc import ABC, abstractmethod

from .BaseModel import BaseModel

class BaseChecker(ABC):
    """各种形式缺陷检查的基类"""

    @abstractmethod
    def __init__(self, data: BaseModel) -> None:
        self._data = data
    @property
    @abstractmethod
    def name(self) -> str:
        """检查器的名称，用于指示所检查的形式缺陷类型"""

    @abstractmethod
    def check(self, **kwargs):
        """针对传递的数据进行特定缺陷的检查"""