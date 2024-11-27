from dataclasses import dataclass
import re

SPLIT_CLAIM = r"^(\d+)\.\s*([^，]+)，.+?(?:\n|$)(?:^[^\d].+?(?:\n|$))*"
TITLE = r"(?:根据|如)权利(?:要求)?(.+?)所述的?(.+)"


@dataclass
class Claim:
    number: int
    dependency: str | None
    is_dependent: bool
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

            dependency, is_dependent, title = self._parse_title(
                raw_title, title_pattern
            )

            claim = Claim(number, dependency, is_dependent, title, content, start_pos)

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
