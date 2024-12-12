import hanlp

from typing import TypeAlias

Tokens: TypeAlias = list[str]
Positions: TypeAlias = list[tuple[int, int]]


class NLPModel:
    def __init__(self, text: str) -> None:
        self._text = text

        self.tokenizer = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
        self.tokenizer.config.output_spans = True

        self.pos_tagger = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
        self.dep_parser = hanlp.load(hanlp.pretrained.dep.CTB9_DEP_ELECTRA_SMALL)

    def reset_model(self, text: str) -> None:
        self._text = text

    def get_tokens(self) -> tuple[Tokens, Positions]:
        tokens, starts, ends = zip(*self.tokenizer(self._text))
        return list(tokens), list(zip(starts, ends))

    def get_pos_tags(self, tokens: Tokens) -> list[str]:
        return self.pos_tagger(tokens)

    def get_deps(self, tokens: Tokens):
        return self.dep_parser(tokens)

    def extract_terms(self) -> dict[str, Positions]:
        tokens, positions = self.get_tokens()
        deps = self.get_deps(tokens)

        term_tag = ["nn", "dobj", "nsubj"]

        for dep in deps:
            if dep["form"] == "所":
                pass
