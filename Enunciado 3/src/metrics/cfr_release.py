"""Change failure rate — variante (b): classificador de release corretiva (PLAN T14).

Uma release é *corretiva* quando existe para corrigir algo que a release
anterior quebrou. Três versões da heurística, todas funções puras (sem I/O):

* **v1** — corretiva se, frente à release anterior, só o ``PATCH`` do SemVer
  mudou (``MAJOR`` e ``MINOR`` iguais, ``PATCH`` maior);
* **v2** — v1 **ou** algum commit da release com mensagem contendo uma das
  palavras-chave (``fix``, ``revert``, ``hotfix``; sem diferenciar maiúsculas);
* **v3** — pontuação ``1 · patch_only + 2 · fração de commits com palavra-chave``,
  corretiva se a pontuação for ≥ ``cutoff`` (tunável).

A escolha da melhor combinação contra o rótulo de consenso fica em
``scripts/tune_cfr.py``.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

DEFAULT_KEYWORDS = ("fix", "revert", "hotfix")
PATCH_WEIGHT = 1.0
KEYWORD_WEIGHT = 2.0

# Primeiro "X.Y" ou "X.Y.Z" da tag; tolera prefixos (v, rel/v, release-) e sufixos (-beta).
_SEMVER = re.compile(r"(?<![\d.])(\d+)\.(\d+)(?:\.(\d+))?")


def semver(tag: str | None) -> tuple[int, int, int] | None:
    """``(major, minor, patch)`` extraído da tag, ou ``None`` se não houver versão."""
    match = _SEMVER.search(tag or "")
    if match is None:
        return None
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch or 0)


def is_patch_only(tag: str | None, previous_tag: str | None) -> bool:
    """v1: mesma ``MAJOR.MINOR`` da release anterior e ``PATCH`` maior."""
    current, previous = semver(tag), semver(previous_tag)
    if current is None or previous is None:
        return False
    return current[:2] == previous[:2] and current[2] > previous[2]


def keyword_pattern(
    keywords: Sequence[str] = DEFAULT_KEYWORDS, *, whole_word: bool = False
) -> re.Pattern[str]:
    """Regex case-insensitive; ``whole_word`` evita casar ``prefix`` com ``fix``."""
    alternatives = "|".join(re.escape(k) for k in keywords)
    body = rf"\b(?:{alternatives})\w*" if whole_word else rf"(?:{alternatives})"
    return re.compile(body, re.IGNORECASE)


def keyword_ratio(messages: Iterable[str] | None, pattern: re.Pattern[str]) -> float:
    """Fração das mensagens de commit que casam com ``pattern`` (0 sem commits)."""
    if messages is None:
        return 0.0
    messages = list(messages)
    if not messages:
        return 0.0
    return sum(bool(pattern.search(m or "")) for m in messages) / len(messages)


def v1(tag: str | None, previous_tag: str | None) -> bool:
    return is_patch_only(tag, previous_tag)


def v2(tag: str | None, previous_tag: str | None, ratio: float) -> bool:
    return is_patch_only(tag, previous_tag) or ratio > 0


def v3_score(tag: str | None, previous_tag: str | None, ratio: float) -> float:
    return PATCH_WEIGHT * is_patch_only(tag, previous_tag) + KEYWORD_WEIGHT * ratio


def v3(tag: str | None, previous_tag: str | None, ratio: float, cutoff: float) -> bool:
    return v3_score(tag, previous_tag, ratio) >= cutoff


@dataclass(frozen=True)
class Scores:
    tp: int
    fp: int
    fn: int
    tn: int

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if p + r else 0.0


def evaluate(predicted: Sequence[bool], expected: Sequence[bool]) -> Scores:
    """Matriz de confusão com "corretiva" como classe positiva."""
    if len(predicted) != len(expected):
        raise ValueError("predicted e expected com tamanhos diferentes")
    pairs = list(zip(predicted, expected, strict=True))
    return Scores(
        tp=sum(p and e for p, e in pairs),
        fp=sum(p and not e for p, e in pairs),
        fn=sum(not p and e for p, e in pairs),
        tn=sum(not p and not e for p, e in pairs),
    )
