from collections import defaultdict
from typing import TypeVar
from ..core import BaseChecker

CheckT = TypeVar("CheckT", bound=BaseChecker)


class CheckManager:
    checkers = defaultdict(list)

    @classmethod
    def register(cls, kind: str):
        def inner_wrapper(other: type[CheckT]) -> type[CheckT]:
            if other not in cls.checkers[kind]:
                cls.checkers[kind].append(other)
            return other

        return inner_wrapper

    def register_checker(self, kind: str, checker: type[BaseChecker]):
        if checker not in self.checkers[kind]:
            self.checkers[kind].append(checker)

    def unregister_checker(self, kind: str, checker: type[BaseChecker]):
        if checker in self.checkers[kind]:
            self.checkers[kind].remove(checker)
