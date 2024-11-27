from dataclasses import dataclass
import re

SPLIT_CLAIM = r"^(\d+)\.\s*([^，]+)，.+?(?:\n|$)(?:^[^\d].+?(?:\n|$))*"
TITLE = r"(?:根据|如)权利(?:要求)?(.+?)所述的?(.+)"


@dataclass
class Claim:
    number: int
    dependency: list[int]
    is_dependent: bool
    is_alternative: bool | None
    title: str
    content: str
    start_pos: int


class ClaimModel:
    def __init__(self, claims: str):
        self._claims = claims

        self.claims = self._parse_claims()

    def _parse_claims(self) -> list[Claim]:
        claims = []
        split_claim_pattern = re.compile(SPLIT_CLAIM, re.DOTALL | re.MULTILINE)
        title_pattern = re.compile(TITLE)

        for match in split_claim_pattern.finditer(self._claims):
            number = int(match.group(1))
            start_pos = match.start()
            raw_title = match.group(2).strip()
            content = match.group()

            deps, is_dependent, title = self._parse_title(
                raw_title, title_pattern
            )

            dependency, is_alternative = self._parse_dependency(deps)

            claim = Claim(number, dependency, is_dependent, is_alternative, title, content, start_pos)

            claims.append(claim)

        return claims

    def _parse_title(
        self, raw_title: str, pattern: re.Pattern
    ) -> tuple[str|None, bool, str]:
        match = pattern.match(raw_title)

        if match is None:
            return None, False, raw_title
        else:
            return match.group(1), True, match.group(2)

    def _parse_dependency(self, deps: str | None) -> tuple[list[int], bool|None]:
        OR_PATTERN = r"(?:\d+[、，或])*\d+或\d+"
        AND_PATTERN = r"((?:\d+[、，和及])*\d+[和及]\d+).*?(任一|任意一)?.*"
        RANGE_PATTERN = r"(\d+)\s*[-~至到]\s*(\d+).*?(任一|任意一)?.*"
        if deps is None:
            return [], None
        elif deps.isdigit():
            return [int(deps)], True
        elif re.match(OR_PATTERN, deps):
            return [int(i) for i in re.split("[、，或]", deps)], True
        elif (match := re.match(AND_PATTERN, deps)):
            return [int(i) for i in re.split("[、，和]", match.group(1))], match.group(2) is not None
        elif (match := re.match(RANGE_PATTERN, deps)):
            return list(range(int(match.group(1)), int(match.group(2)) + 1)), match.group(3) is not None
        else:
            raise ValueError(f"权利要求引用撰写方式:`{deps}`未被处理, 请反馈Bug")
