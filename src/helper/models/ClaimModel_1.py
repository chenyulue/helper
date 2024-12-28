import re

from ..core.BaseModel import BaseModel


class ClaimModel(BaseModel):
    """ClaimModel类用于解析权利要求"""

    def __init__(self, pattern: re.Pattern, content: str) -> None:
        pass
