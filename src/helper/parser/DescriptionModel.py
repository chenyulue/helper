from ..core.BaseModel import BaseModel

class DescriptionModel(BaseModel):
    def __init__(self, data: str):
        super().__init__(data)

    def parse(self):
        pass

    def reset_model(self, data: str) -> None:
        self._data = data