from dataclasses import dataclass
import re

@dataclass
class Claim:
    number: int
    dependency: list[int]
    is_dependent: bool
    title: str
    content: str
    start_pos: int

class ClaimModel:
    def __init__(self, claims: str):
        self._claims = claims

    def _parse_claims(self) -> list[Claim]:
        pass