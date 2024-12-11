from dataclasses import dataclass
import re
import itertools
from typing import Literal, TypeAlias, Any

SPLIT_CLAIM = r"^(\d+)\.\s*([^，]+)，.+?(?:\n|$)(?:^[^\d\n].+?(?:\n|$))*"
TITLE = r"(?:根据|如)权?利?要?求?(.+?)所述的?(.+)"

TITLE_WITHOUT_DOMAIN = "一种装置|一种方法|一种工艺"

SMALL_DEFECTS: TypeAlias = Literal[
    "non_alternative_reference", "no_title_domain", "claim_phrases_unintegrity"
]


@dataclass
class Claim:
    """权利要求类，由解析权利要求生成

    Parameters
    -------
    number: int
        权利要求编号
    dependency: list[int]
        引用的权利要求编号
    is_dependent: bool
        独立权利要求为False，从属权利要求为True
    is_alternative: bool | None
        从属权利要求中，择一引用为True，非择一引用为False；对于独立权利要求，其值为None
    title: str
        权利要求的主题名称，其中独立权利要求为第一个逗号之前整个主题名称部分，而从属权利要求则为
        “所述”等表述后的主题部分
    content: str
        该项权利要求的原始文本
    start_pos: int
        该项权利要求在原始权利要求文本中位置
    """

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
    """缺乏引用基础的技术特征的相关信息

    Parameters
    ----------
    position : int
        缺乏引用基础的相关特征表述在原始权利要求中的位置，记录“所述”开始的位置
    term: str
        缺乏引用基础的相关特征术语，即“所述”之后的特征
    context: str
        缺乏引用基础的相关特征的上下文文本，从该“所述”等引用词开始直至下一个标点符号或者下一个“所述”等引用词的文本范围
    hasbasis_checked: bool | list[int]
        程序检查的缺乏引用基础问题的结果，所有引用路径都有引用基础则为True，所有引用路径都没有引用基础则为False，
        部分引用路径有引用基础则记录这些引用引用基础的部分引用路径。
    """

    position: int
    term: str
    context: str
    hasbasis_confirmed: bool | None
    hasbasis_checked: bool | list[int]


class RefBasisConfirmed:
    def __init__(self, has_basis: set[int]=set(), lack_basis: set[int]=set()):
        self.has_basis = set()
        self.lack_basis = set()

    def __str__(self):
        return f"has basis: {self.has_basis}, lack basis: {self.lack_basis}"


class ClaimModel:
    def __init__(self, claims: str):
        self._claims = claims

        self.claims = self._parse_claims()

        # 缺少引用基础缺陷结果
        self.reference_basis: dict[int, dict[int, RefBasis]] = {}
        self.reference_basis_confirmed = RefBasisConfirmed()
        self.reference_path: dict[int, list[int]] = {}

        # 多引多缺陷结果
        self.multiple_dependencies: dict[int, list[int]] | None = None

        # 非择一引用缺陷结果、主题名称为体现技术领域及“权利要求”这4个字不完整
        self.small_defects: dict[SMALL_DEFECTS, list[Any]] = {}

    def reset_model(self, new_claims: str) -> None:
        """根据新的权利要求文本重置ClaimModel：重新解析权利要求，并将相关的缺陷查询结果清空

        Parameters
        ----------
        new_claims : str
            新的权利要求文本
        """
        self.__init__(new_claims)

    def clear_reference_basis(self):
        self.reference_basis = {}

    # =========================== 解析权利要求 ===========================
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
        # 修改此处的正则表达式时，注意同步修改下面各条件分支中的表达
        OR_PATTERN = r"(?:\d+[、，或])*\d+或\d+"
        AND_PATTERN = r"((?:\d+[、，和及])*\d+[和及]\d+)(.*任意?一)?.*"
        RANGE_PATTERN = r"(\d+)\s*[-~至到]\s*(\d+)(.*任意?一)?.*"

        if deps is not None:
            deps = deps.strip()

        if deps is None:
            return [], None
        elif deps.isdigit():
            return [int(deps)], True
        elif re.match(OR_PATTERN, deps):
            return [int(i) for i in re.split("[、，或]", deps)], True
        elif match := re.match(AND_PATTERN, deps):
            return [
                int(i) for i in re.split("[、，和及]", match.group(1))
            ], match.group(2) is not None
        elif match := re.match(RANGE_PATTERN, deps):
            return list(
                range(int(match.group(1)), int(match.group(2)) + 1)
            ), match.group(3) is not None
        else:
            raise ValueError(
                f"权项编号引用撰写方式: “<b>{deps}</b>” 未被处理, <br>未能正确解析权利要求请反馈Bug"
            )

    # ============================ 检查引用基础的缺陷 =======================
    def check_all_reference_basis(self, length: int) -> None:
        """该函数根据特定的截词长度，检查权利要求书中所有缺乏引用基础的缺陷，相应的结果收集在`self.reference_basis`字典中，
        其中，key是权利要求编号，value是针对每个权利要求的引用缺陷dict。在该引用缺陷dict中，其key值为该权利要求中存在*所述*
        等表述的技术特征在原始权利要求文本中的位置（用于后续在原始权利要求中定位并格式化相关特征表述），而value值是一个RefBais
        对象，其记录缺乏引用基础的相关信息。

        Parameters
        ----------
        length : int
            技术术语的截词长度
        """
        for claim in self.claims:
            self._check_reference_basis(claim, length)

    def get_all_reference_paths(self) -> dict[int, list[int]]:
        """获取所有权利要求的引用路径"""
        for i, claim in enumerate(self.claims):
            paths = self._flatten_paths(self._get_reference_path(i + 1, self.claims))
            self.reference_path[i + 1] = paths[1:]
        return self.reference_path

    def _check_reference_basis(self, claim: Claim, length: int) -> None:
        for term, position in self._get_terminology(claim, length).items():
            pos = claim.start_pos + position[0]
            result = self._reference_has_basis(claim, term, position[0], self.claims)
            if self.reference_basis.get(claim.number) is None:
                self.reference_basis[claim.number] = {
                    pos: RefBasis(pos, term, position[1], None, result)
                }
            else:
                self.reference_basis[claim.number].update(
                    {pos: RefBasis(pos, term, position[1], None, result)}
                )

    def _get_terminology(self, claim: Claim, length: int) -> dict[str, tuple[int, str]]:
        preceding_words = "所述的?|上述的?|前述的?|该些?"
        PATTERN = (
            "(?:"
            f"{preceding_words})"
            "([^，。；,;]{1,"
            f"{length}"
            "}).*?(?=[，。；,;、]|"
            f"{preceding_words})"
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
                # existed_ref = ref_number

                # 如果所有的引用路径上都存在该术语，则直接返回True
                if all(ref_number in paths for paths in ref_paths):
                    return True
                # 收集存在该术语的部分引用路径
                else:
                    existed_refs.append(ref_number)

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

    # ====================== 检查多引多的缺陷 ============================
    def check_all_multiple_dependencies(self) -> None:
        """检查多引多缺陷，检查结果为一个dict，其中key为存在多引多缺陷的权项，
        value 为所引用的多项从属权利要求。
        """
        if self.multiple_dependencies is None:
            self.multiple_dependencies = {
                claim.number: result[1]
                for claim in self.claims
                if (result := self._check_multiple_dependencies(claim))[0]
            }

    def _check_multiple_dependencies(self, claim: Claim) -> tuple[bool, list[int]]:
        if len(claim.dependency) > 1:
            multiple_dependencies = [
                ref
                for ref in claim.dependency
                if len(self.claims[ref - 1].dependency) > 1
            ]
            return len(multiple_dependencies) > 0, multiple_dependencies
        return False, []

    # ======================= 检查非择一引用缺陷 =============================
    def check_all_alternative_reference(self) -> list[int]:
        """检查所有从属权利要求中非择一引用的问题

        Returns
        -------
        list[int]
            存在非择一引用缺陷的所有权利要求编号
        """
        if self.small_defects.get("non_alternative_reference") is None:
            result = [
                claim.number for claim in self.claims if claim.is_alternative is False
            ]
            if result:
                self.small_defects["non_alternative_reference"] = result
        return self.small_defects.get("non_alternative_reference", [])

    # ======================= 检查主题名称未体现技术领域 =======================
    def check_all_title_domain(self) -> list[int]:
        """检索权利要求中主题名称未体现技术领域的缺陷

        Returns
        -------
        list[int]
            存在技术主题名称未体现技术领域缺陷的权利要求编号
        """
        if self.small_defects.get("no_title_domain") is None:
            result = [
                claim.number
                for claim in self.claims
                if (
                    claim.is_dependent is False
                    and re.match(TITLE_WITHOUT_DOMAIN, claim.title) is not None
                )
            ]
            if result:
                self.small_defects["no_title_domain"] = result
        return self.small_defects.get("no_title_domain", [])

    # ================ 检查权利要求主题文本中“权利要求”4个字是否完整 ================
    def check_all_claim_phrases_integrity(self) -> list[tuple[int, str]]:
        """检查权利要求主题文本中“权利要求”这4个字是否完整

        Returns
        -------
        list[tuple[int, str]]
            “权利要求”这4个字不完整的的权利要求编号及相应不完整的表述
        """
        if self.small_defects.get("claim_phrases_unintegrity") is None:
            pattern = r"(?:根据|如)(权?)(利?)(要?)(求?)\d+.*?所述"
            regex = re.compile(pattern)

            result = []
            for claim in self.claims:
                m = regex.search(claim.content)
                if m is not None and (phrase := "".join(m.groups())) != "权利要求":
                    result.append((claim.number, phrase))
            if result:
                self.small_defects["claim_phrases_unintegrity"] = result
        return self.small_defects.get("claim_phrases_unintegrity", [])

    # ======================= 检查权利要求中涉嫌不清楚以及敏感的词 =======================
    def check_all_indefinite_expression(self) -> None:
        pass

    def check_all_sensitive_expressioin(self) -> None:
        pass
