from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract method for all models."""

    @abstractmethod
    def parse(self, data: str) -> None:
        """Parse the text data."""
        pass