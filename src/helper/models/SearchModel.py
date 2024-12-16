import re

class SearchModel:
    def __init__(self, pattern: str, *args):
        self._pattern = re.compile(pattern, *args)

    def reset_pattern(self, pattern: str, *args):
        self.__init__(pattern, *args)

    def search(self, text: str) -> dict[str, list[tuple[int, int]]]:
        start: int = 0
        result = {}
        for match in self._pattern.finditer(text, start):
            term = match.group()
            if term not in result:
                result[term] = [match.span()]
            else:
                result[term].append(match.span())
        return result
