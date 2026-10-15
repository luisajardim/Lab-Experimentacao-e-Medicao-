#!/usr/bin/env python3
"""Tuning da heurística CFR(b) contra o rótulo de consenso (PLAN T14).

Para cada release da amostra-ouro (``corrective_1..5`` de
``labels_consensus.csv``) monta: tag, tag da release anterior (ordem
cronológica, a mesma dos dossiês) e mensagens dos commits desde ela. Depois
testa todas as combinações abaixo e escolhe a de maior F1 (empates: a primeira
na ordem v1 → v2 → v3, ou seja, a mais simples):

* v1;
* v2 × conjunto de palavras-chave × casamento (substring | palavra inteira);
* v3 × conjunto de palavras-chave × casamento × corte.

Itens com consenso vazio (empate pendente) ficam de fora. Releases sem commits
coletados contam como "sem palavra-chave".

Saídas
------
* ``data/gold/cfr_metrics.json``: melhor combinação com precisão, recall e F1;
* ``docs/cfr_heuristic_history.md``: tabela de todas as combinações testadas,
  reescrita entre os marcadores ``<!-- tuning:start -->`` e
  ``<!-- tuning:end -->`` (o texto fora deles é preservado).

Código de saída: 0 se F1 ≥ 0,70; 1 se abaixo da meta; 2 em erro de entrada.

Uso
---
    python scripts/tune_cfr.py
    python scripts/tune_cfr.py --consensus data/gold/labels_consensus.csv --input-dir data/gold
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Mesma leitura dos JSONs que gerou os dossiês vistos pelos avaliadores.
from build_dossiers import (  # noqa: E402
    _commit_message,
    _commits_for,
    _previous_release,
    load_records,
)
from label_tool import CORRECTIVE_COLUMNS, read_csv  # noqa: E402

from metrics import cfr_release  # noqa: E402

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DEFAULT_CONSENSUS = GOLD_DIR / "labels_consensus.csv"
DEFAULT_INPUT_DIRS = (GOLD_DIR,)
DEFAULT_METRICS = GOLD_DIR / "cfr_metrics.json"
DEFAULT_HISTORY = PROJECT_ROOT / "docs" / "cfr_heuristic_history.md"

TARGET_F1 = 0.70
KEYWORD_SETS: dict[str, tuple[str, ...]] = {
    "base": cfr_release.DEFAULT_KEYWORDS,
    "ampliado": (*cfr_release.DEFAULT_KEYWORDS, "bug", "patch", "regression", "crash"),
}
MATCH_MODES = {"substring": False, "palavra": True}
CUTOFFS = tuple(round(0.25 * step, 2) for step in range(1, 13))  # 0,25 .. 3,00
FEATURE_WEIGHTS = (0.0, 1.0, 2.0)  # penalidade da v4 para commits ``feat``
CV_FOLDS = 5
CV_REPEATS = 20

START_MARKER = "<!-- tuning:start -->"
END_MARKER = "<!-- tuning:end -->"


@dataclass(frozen=True)
class Item:
    full_name: str
    tag: str | None
    previous_tag: str | None
    messages: tuple[str, ...] | None  # None = commits não coletados
    expected: bool


@dataclass(frozen=True)
class Candidate:
    version: str
    keywords: str | None = None
    match: str | None = None
    cutoff: float | None = None
    feature_weight: float | None = None

    @property
    def name(self) -> str:
        parts = [self.version]
        if self.keywords:
            parts += [f"kw={self.keywords}", f"match={self.match}"]
        if self.feature_weight is not None:
            parts.append(f"feat=-{self.feature_weight:g}")
        if self.cutoff is not None:
            parts.append(f"corte={self.cutoff:.2f}")
        return " ".join(parts)


def load_items(consensus_path: Path, input_dirs: Sequence[Path]) -> list[Item]:
    records = load_records(input_dirs)
    items: list[Item] = []
    missing: list[str] = []
    for row in read_csv(consensus_path):
        payload = records.get(row["full_name"])
        for index, column in enumerate(CORRECTIVE_COLUMNS, start=1):
            label = (row.get(column) or "").strip()
            if label not in ("sim", "não"):
                continue  # empate ainda pendente no consenso
            url = row[f"release_url_{index}"]
            release = next(
                (r for r in (payload or {}).get("releases", []) if r.get("html_url") == url),
                None,
            )
            if release is None:
                missing.append(url)
                continue
            previous = _previous_release(payload, release)
            commits = _commits_for(payload, release)
            items.append(
                Item(
                    full_name=row["full_name"],
                    tag=release.get("tag_name"),
                    previous_tag=previous.get("tag_name") if previous else None,
                    messages=None if commits is None else tuple(map(_commit_message, commits)),
                    expected=label == "sim",
                )
            )
    if missing:
        raise ValueError(f"{len(missing)} release(s) do consenso sem JSON, ex.: {missing[:3]}")
    if not items:
        raise ValueError(f"nenhum item rotulado em {consensus_path}")
    return items


def candidates() -> list[Candidate]:
    result = [Candidate("v1")]
    for version in ("v2", "v3"):
        for keywords in KEYWORD_SETS:
            for match in MATCH_MODES:
                if version == "v2":
                    result.append(Candidate(version, keywords, match))
                else:
                    result += [Candidate(version, keywords, match, c) for c in CUTOFFS]
    for keywords in KEYWORD_SETS:
        for match in MATCH_MODES:
            for weight in FEATURE_WEIGHTS:
                result += [Candidate("v4", keywords, match, c, weight) for c in CUTOFFS]
    return result


def predict(candidate: Candidate, items: Sequence[Item]) -> list[bool]:
    if candidate.version == "v1":
        return [cfr_release.v1(i.tag, i.previous_tag) for i in items]
    pattern = cfr_release.keyword_pattern(
        KEYWORD_SETS[candidate.keywords], whole_word=MATCH_MODES[candidate.match]
    )
    ratios = [cfr_release.keyword_ratio(i.messages, pattern) for i in items]
    if candidate.version == "v2":
        return [cfr_release.v2(i.tag, i.previous_tag, r) for i, r in zip(items, ratios, strict=True)]
    if candidate.version == "v3":
        return [
            cfr_release.v3(i.tag, i.previous_tag, r, candidate.cutoff)
            for i, r in zip(items, ratios, strict=True)
        ]
    return [
        cfr_release.v4(
            i.tag,
            r,
            cfr_release.has_feature_commit(i.messages),
            candidate.feature_weight,
            candidate.cutoff,
        )
        for i, r in zip(items, ratios, strict=True)
    ]


def tune(items: Sequence[Item]) -> list[tuple[Candidate, cfr_release.Scores]]:
    expected = [i.expected for i in items]
    return [(c, cfr_release.evaluate(predict(c, items), expected)) for c in candidates()]


def best_of(results: Sequence[tuple[Candidate, cfr_release.Scores]]):
    return max(results, key=lambda pair: pair[1].f1)  # max devolve o primeiro empatado


def cross_validate(items: Sequence[Item]) -> dict[str, float]:
    """F1 fora da amostra: escolhe a combinação nos repositórios de treino e
    avalia nos repositórios deixados de fora (k-fold por repositório, repetido).

    Mede quanto do F1 da seleção na amostra inteira é otimismo do tuning.
    """
    expected = [i.expected for i in items]
    predictions = [predict(c, items) for c in candidates()]
    repos = sorted({i.full_name for i in items})
    scores = []
    for seed in range(CV_REPEATS):
        shuffled = repos[:]
        random.Random(seed).shuffle(shuffled)
        out_of_fold: list[bool] = [False] * len(items)
        for fold in range(CV_FOLDS):
            held_out = set(shuffled[fold::CV_FOLDS])
            train = [k for k, i in enumerate(items) if i.full_name not in held_out]
            test = [k for k, i in enumerate(items) if i.full_name in held_out]
            best = max(
                predictions,
                key=lambda p: cfr_release.evaluate(
                    [p[k] for k in train], [expected[k] for k in train]
                ).f1,
            )
            for k in test:
                out_of_fold[k] = best[k]
        scores.append(cfr_release.evaluate(out_of_fold, expected).f1)
    return {
        "folds": CV_FOLDS,
        "repeats": CV_REPEATS,
        "f1_mean": round(sum(scores) / len(scores), 4),
        "f1_min": round(min(scores), 4),
        "f1_max": round(max(scores), 4),
    }


def coverage(items: Sequence[Item]) -> dict[str, int]:
    return {
        "items": len(items),
        "positives": sum(i.expected for i in items),
        "items_with_commits": sum(i.messages is not None for i in items),
        "items_with_previous_release": sum(i.previous_tag is not None for i in items),
    }


def best_per_version(results) -> dict[str, tuple[Candidate, cfr_release.Scores]]:
    versions = dict.fromkeys(c.version for c, _ in results)
    return {v: best_of([pair for pair in results if pair[0].version == v]) for v in versions}


def metrics_payload(
    results, items: Sequence[Item], cv: dict[str, float] | None = None
) -> dict[str, Any]:
    candidate, scores = best_of(results)
    return {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "target_f1": TARGET_F1,
        "meets_target": scores.f1 >= TARGET_F1,
        "best": {
            "name": candidate.name,
            **asdict(candidate),
            "keyword_list": list(KEYWORD_SETS[candidate.keywords]) if candidate.keywords else None,
            "precision": round(scores.precision, 4),
            "recall": round(scores.recall, 4),
            "f1": round(scores.f1, 4),
            **asdict(scores),
        },
        "best_per_version": {
            version: {"name": c.name, "f1": round(s.f1, 4)}
            for version, (c, s) in best_per_version(results).items()
        },
        "cross_validation": cv,
        "candidates_tested": len(results),
        **coverage(items),
    }


def render_history(results, items: Sequence[Item], payload: dict[str, Any]) -> str:
    cov = coverage(items)
    best = payload["best"]
    lines = [
        START_MARKER,
        f"## Execução de {payload['generated_at']}",
        "",
        "Gerado por `scripts/tune_cfr.py`; o texto entre os marcadores é reescrito a cada execução.",
        "",
        f"- Itens (releases com consenso): {cov['items']} ({cov['positives']} corretivas)",
        f"- Com commits coletados: {cov['items_with_commits']}; "
        f"com release anterior: {cov['items_with_previous_release']}",
        "- Palavras-chave: "
        + "; ".join(f"`{k}` = {', '.join(v)}" for k, v in KEYWORD_SETS.items()),
        f"- **Melhor: {best['name']}** — precisão {best['precision']:.3f}, "
        f"recall {best['recall']:.3f}, F1 {best['f1']:.3f} "
        f"({'atinge' if payload['meets_target'] else 'NÃO atinge'} a meta de {TARGET_F1:.2f})",
    ]
    cv = payload.get("cross_validation")
    if cv:
        lines.append(
            f"- F1 fora da amostra ({cv['folds']}-fold por repositório, {cv['repeats']} "
            f"repetições): média {cv['f1_mean']:.3f} (mín. {cv['f1_min']:.3f}, "
            f"máx. {cv['f1_max']:.3f})"
        )
    lines += [
        "",
        "### Melhor combinação de cada versão",
        "",
        "| Versão | Combinação | F1 |",
        "|---|---|---:|",
        *(
            f"| {version} | {entry['name']} | {entry['f1']:.3f} |"
            for version, entry in payload["best_per_version"].items()
        ),
        "",
        "### Todas as combinações",
        "",
        "| Combinação | Precisão | Recall | F1 | TP | FP | FN | TN |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for candidate, s in results:
        lines.append(
            f"| {candidate.name} | {s.precision:.3f} | {s.recall:.3f} | {s.f1:.3f} "
            f"| {s.tp} | {s.fp} | {s.fn} | {s.tn} |"
        )
    lines.append(END_MARKER)
    return "\n".join(lines)


def write_history(path: Path, section: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if START_MARKER in text and END_MARKER in text:
        head, rest = text.split(START_MARKER, 1)
        tail = rest.split(END_MARKER, 1)[1]
        text = head + section + tail
    else:
        text = text.rstrip() + ("\n\n" if text else "") + section + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(args: argparse.Namespace) -> int:
    if not args.consensus.exists():
        raise ValueError(f"{args.consensus} não existe; rode scripts/agreement.py antes (T13)")
    items = load_items(args.consensus, args.input_dir)
    results = tune(items)
    payload = metrics_payload(results, items, cross_validate(items))

    args.metrics.parent.mkdir(parents=True, exist_ok=True)
    args.metrics.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_history(args.history, render_history(results, items, payload))

    best = payload["best"]
    print(f"{len(results)} combinações em {payload['items']} releases "
          f"({payload['items_with_commits']} com commits)")
    print(f"melhor: {best['name']}  P={best['precision']:.3f} R={best['recall']:.3f} "
          f"F1={best['f1']:.3f}  meta {TARGET_F1:.2f}: {'ok' if payload['meets_target'] else 'NÃO'}")
    print(f"F1 fora da amostra (media CV): {payload['cross_validation']['f1_mean']:.3f}")
    return 0 if payload["meets_target"] else 1


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--consensus", type=Path, default=DEFAULT_CONSENSUS)
    parser.add_argument("--input-dir", type=Path, action="append")
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    args = parser.parse_args(argv)
    args.input_dir = args.input_dir or list(DEFAULT_INPUT_DIRS)
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(args)
    except (OSError, KeyError, ValueError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
