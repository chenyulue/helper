from collections.abc import Iterator
from typing import Literal, TypeAlias

from cydifflib import SequenceMatcher # type: ignore

OpCode: TypeAlias = Literal["equal", "replace", "delete", "insert"]

class CmpModel(SequenceMatcher):
    def __init__(self, a: str="", b: str="") -> None:
        super().__init__(a=a, b=b, autojunk=False)

    def compare(self) -> Iterator[tuple[OpCode, int, int, int, int]]:
        for codes in self.get_opcodes():
            yield codes