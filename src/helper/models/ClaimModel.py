from dataclasses import dataclass
import re
import itertools

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

    def __eq__(self, other):
        if not isinstance(other, Claim):
            return False
        return self.content == other.content

    def __hash__(self):
        return hash(self.content)


@dataclass
class RefBasis:
    position: int
    term: str
    context: str
    hasbasis_confirmed: bool | None
    hasbasis_checked: bool | list[int]


class ClaimModel:
    def __init__(self, claims: str):
        self._claims = claims

        self.claims = self._parse_claims()

        self.reference_basis = {}
        self.reference_path = {}

    def reset_model(self, new_claims: str) -> None:
        """根据新的权利要求文本重置ClaimModel：重新解析权利要求，并将引用基础赋值空列表

        Parameters
        ----------
        new_claims : str
            新的权利要求文本
        """
        self._claims = new_claims
        self.claims = self._parse_claims()
        self.reference_basis = {}
        self.reference_path = {}

    def _parse_claims(self) -> tuple[Claim, ...]:
        claims = []
        split_claim_pattern = re.compile(SPLIT_CLAIM, re.DOTALL | re.MULTILINE)
        title_pattern = re.compile(TITLE)

        for match in split_claim_pattern.finditer(self._claims):
            number = int(match.group(1))
            start_pos = match.start()
            raw_title = match.group(2).strip()
            content = match.group()

            deps, is_dependent, title = self._parse_title(raw_title, title_pattern)

            dependency, is_alternative = self._parse_dependency(deps)

            claim = Claim(
                number,
                dependency,
                is_dependent,
                is_alternative,
                title,
                content,
                start_pos,
            )

            claims.append(claim)

        return tuple(claims)

    def _parse_title(
        self, raw_title: str, pattern: re.Pattern
    ) -> tuple[str | None, bool, str]:
        match = pattern.match(raw_title)

        if match is None:
            return None, False, raw_title
        else:
            return match.group(1), True, match.group(2)

    def _parse_dependency(self, deps: str | None) -> tuple[list[int], bool | None]:
        OR_PATTERN = r"(?:\d+[、，或])*\d+或\d+"
        AND_PATTERN = r"((?:\d+[、，和及])*\d+[和及]\d+).*?(任一|任意一)?.*"
        RANGE_PATTERN = r"(\d+)\s*[-~至到]\s*(\d+).*?(任一|任意一)?.*"
        if deps is None:
            return [], None
        elif deps.isdigit():
            return [int(deps)], True
        elif re.match(OR_PATTERN, deps):
            return [int(i) for i in re.split("[、，或]", deps)], True
        elif match := re.match(AND_PATTERN, deps):
            return [int(i) for i in re.split("[、，和]", match.group(1))], match.group(
                2
            ) is not None
        elif match := re.match(RANGE_PATTERN, deps):
            return list(
                range(int(match.group(1)), int(match.group(2)) + 1)
            ), match.group(3) is not None
        else:
            raise ValueError(f"权利要求引用撰写方式:`{deps}`未被处理, 请反馈Bug")

    def check_all_reference_basis(self, length: int) -> None:
        """该函数根据特定的截词长度，检查权利要求书中所有缺乏引用基础的缺陷

        Parameters
        ----------
        length : int
            技术术语的截词长度
        """
        for claim in self.claims:
            self._check_reference_basis(claim, length)

    def get_all_reference_paths(self) -> None:
        """获取所有权利要求的引用路径"""
        for i, claim in enumerate(self.claims):
            paths = self._flatten_paths(
                self._get_reference_path(i + 1, self.claims)
            )
            self.reference_path[i+1] = paths[1:]

    def _check_reference_basis(self, claim: Claim, length: int) -> None:
        for term, position in self._get_terminology(claim, length).items():
            pos = claim.start_pos + position[0]
            if self.reference_basis.get(claim.number) is None:
                result = self._reference_has_basis(
                    claim, term, position[0], self.claims
                )
                self.reference_basis[claim.number] = {
                    pos: RefBasis(pos, term, position[1], None, result)
                }
            elif self.reference_basis[claim.number].get(pos) is None:
                result = self._reference_has_basis(
                    claim, term, position[0], self.claims
                )
                self.reference_basis[claim.number].update(
                    {pos: RefBasis(pos, term, position[1], None, result)}
                )
            elif self.reference_basis[claim.number].get(pos).hasbasis_confirmed is None:
                result = self._reference_has_basis(
                    claim, term, position[0], self.claims
                )
                self.reference_basis[claim.number].update(
                    {pos: RefBasis(pos, term, position[1], None, result)}
                )

    def _get_terminology(self, claim: Claim, length: int) -> dict[str, tuple[int, str]]:
        preceding_words = "所述的?|上述的?|前述的?|该些?)"
        PATTERN = (
            "(?:"
            f"{preceding_words}"
            "([^，。；,;]{1,"
            f"{length}"
            "}).*?(?=[，。；,;]|"
            f"{preceding_words}"
        )
        pattern = re.compile(PATTERN)

        terms = {}
        for match in pattern.finditer(claim.content):
            terms.setdefault(match.group(1), (match.start(), match.group()))

        return terms

    def _reference_has_basis(
        self, claim: Claim, terminology: str, pos: int, claims: tuple[Claim, ...]
    ) -> bool | list[int]:
        pattern = re.compile(terminology)

        # 检查当前权利要求中在该技术术语之前的文本中是否定义了该术语
        if pattern.search(claim.content, 0, pos):
            return True
        # 检查其引用的权利要求中是否定义了该术语
        else:
            return self._terminology_exists(pattern, claim.number, claims)

    def _terminology_exists(
        self, pattern: re.Pattern, claim_number: int, claims: tuple[Claim, ...]
    ) -> bool | list[int]:
        ref_paths = self._get_reference_path(claim_number, claims)

        existed_refs = []
        for ref_number in self._flatten_paths(ref_paths)[1:]:
            ref_claim = self.claims[ref_number - 1]
            if pattern.search(ref_claim.content):
                existed_ref = ref_number

                # 如果所有的引用路径上都存在该术语，则直接返回True
                if all(existed_ref in paths for paths in ref_paths):
                    return True
                # 收集存在该术语的部分引用路径
                else:
                    existed_refs.append(existed_ref)

        # 若existed_refs为空列表，则表明所有引用路径都不存在该技术术语
        return existed_refs if existed_refs else False

    @staticmethod
    def _get_reference_path(
        claim_number: int, claims: tuple[Claim, ...]
    ) -> list[list[int]]:
        # 如果该权利要求没有引用其他权利要求（即为独立权利要求），直接返回编号
        if not claims[claim_number - 1].dependency:
            return [[claim_number]]

        # 否则，递归获取引用的权利要求的路径
        paths = []
        for referenced_claim in claims[claim_number - 1].dependency:
            # 递归获取被引用的权利要求的路径
            sub_paths = ClaimModel._get_reference_path(referenced_claim, claims)

            # 将当前权利要求加入到每个路径的前面
            for path in sub_paths:
                paths.append([claim_number] + path)

        return paths

    def _flatten_paths(self, paths: list[list[int]]) -> list[int]:
        return sorted(set(itertools.chain(*paths)), reverse=True)
