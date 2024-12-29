from abc import ABC, abstractmethod

class BaseModel(ABC):
    """BaseModel为解析文本数据的抽象基类"""

    @abstractmethod
    def __init__(self, data: str) -> None:
        """
        Parameters
        ----------
        data : str
            文本数据
        """
        self._data = data

    @abstractmethod
    def parse(self) -> None:
        """解析文本数据"""

    @abstractmethod
    def reset_model(self, data: str) -> None:
        """传递新文本进行重置数据模型

        Parameters
        ----------
        data : str
            文本数据
        """