from abc import ABC, abstractmethod

from .BaseModel import BaseModel

class BaseChecker(ABC):
    """Base checker for all checkings."""
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the checker, indicating what the defect is.
        """
        pass

    @abstractmethod
    def check(self, data: BaseModel):
        """Check the data for the specific defect."""
        pass