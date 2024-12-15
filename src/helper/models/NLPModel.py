from collections import defaultdict
import hanlp

from typing import TypeAlias

Tokens: TypeAlias = list[str]
Positions: TypeAlias = list[tuple[int, int]]


class NLPModel:
    def __init__(self, text: str) -> None:
        self._text = text

        self.tokenizer = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
        self.tokenizer.config.output_spans = True
        self.tokenizer.dict_combine = {"所述", "所述的"}

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

    def extract_terms(self) -> defaultdict[str, list[int]]:
        tokens, positions = self.get_tokens()
        deps = iter(self.get_deps(tokens))

        term_end_tags = [
            "nn",
            "dobj",
            "pobj",
            "lobj",
            "nsubj",
            "xsubj",
            "nsubjpass",
            "top",
        ]

        terms = defaultdict(list)

        while True:
            try:
                dep = next(deps)
                if dep["form"].startswith("所述"):
                    position = positions[dep["id"] - 1]
                    term_toks = []

                    term_dep = next(deps)
                    while True:
                        if term_dep["id"] <= dep["head"]:
                            term_toks.append(term_dep)
                        elif term_dep["head"] == term_toks[-1]["head"]:
                            term_toks.append(term_dep)
                        elif term_dep["deprel"] in term_end_tags and term_dep["id"] == term_toks[-1]["head"]:
                            term_toks.append(term_dep)
                        else:
                            break
                        term_dep = next(deps)

                    term = "".join(d["form"] for d in term_toks)
                    terms[term].append(position[0])
                    print(term, "at", position)
            except StopIteration:
                break

        return terms
