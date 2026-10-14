from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))  # tune_cfr importa build_dossiers/label_tool
SPEC = importlib.util.spec_from_file_location("tune_cfr", SCRIPTS_DIR / "tune_cfr.py")
assert SPEC and SPEC.loader
tune_cfr = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = tune_cfr
SPEC.loader.exec_module(tune_cfr)

# (tag, mensagens dos commits, corretiva no consenso)
RELEASES = [
    ("v1.0.0", None, "não"),  # primeira release: sem anterior nem commits
    ("v1.0.1", ["fix crash on start"], "sim"),
    ("v1.1.0", ["feat: new api", "add prefix option"], "não"),
    ("v1.2.0", ["Revert broken cache", "hotfix login"], "sim"),
    ("v1.2.1", ["docs typo"], "não"),
    ("v1.3.0", ["feat: export"], "não"),
]


def _gold(tmp_path: Path) -> tuple[Path, Path]:
    name = "org/repo"
    releases = [
        {
            "tag_name": tag,
            "draft": False,
            "prerelease": False,
            "published_at": f"2026-01-{i + 1:02d}T00:00:00Z",
            "html_url": f"https://github.com/{name}/releases/tag/{tag}",
        }
        for i, (tag, _, _) in enumerate(RELEASES)
    ]
    commits_between = [
        {
            "release": tag,
            "previous_release": RELEASES[i - 1][0] if i else None,
            "commits": None if msgs is None else [{"message": m} for m in msgs],
            "ignored_reason": "no_previous_release" if msgs is None else None,
        }
        for i, (tag, msgs, _) in enumerate(RELEASES)
    ]
    gold_dir = tmp_path / "gold"
    (gold_dir / "org").mkdir(parents=True)
    (gold_dir / "org" / "repo.json").write_text(
        json.dumps({"repository": {"full_name": name}, "releases": releases,
                    "commits_between": commits_between}),
        encoding="utf-8",
    )

    consensus = tmp_path / "consensus.csv"
    sampled = RELEASES[1:]  # 5 releases sorteadas
    row = {"full_name": name, "project_type": "outro", "delivers_to_user": "sim"}
    for i, (tag, _, label) in enumerate(sampled, start=1):
        row[f"release_url_{i}"] = f"https://github.com/{name}/releases/tag/{tag}"
        row[f"corrective_{i}"] = label
    row["corrective_5"] = ""  # empate pendente: deve ser ignorado
    with consensus.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    return consensus, gold_dir


def test_load_items_uses_previous_release_and_commits(tmp_path: Path) -> None:
    consensus, gold_dir = _gold(tmp_path)
    items = tune_cfr.load_items(consensus, [gold_dir])
    assert [(i.tag, i.previous_tag, i.expected) for i in items] == [
        ("v1.0.1", "v1.0.0", True),
        ("v1.1.0", "v1.0.1", False),
        ("v1.2.0", "v1.1.0", True),
        ("v1.2.1", "v1.2.0", False),
    ]
    assert items[0].messages == ("fix crash on start",)


def test_candidates_cover_all_versions() -> None:
    names = [c.name for c in tune_cfr.candidates()]
    assert names[0] == "v1"
    assert "v2 kw=base match=substring" in names
    assert "v3 kw=ampliado match=palavra corte=3.00" in names
    assert len(names) == 1 + 4 + 4 * len(tune_cfr.CUTOFFS)


def test_main_selects_best_and_writes_outputs(tmp_path: Path) -> None:
    consensus, gold_dir = _gold(tmp_path)
    metrics = tmp_path / "cfr_metrics.json"
    history = tmp_path / "history.md"
    history.write_text(
        "# Histórico\n\nTexto manual.\n\n<!-- tuning:start -->\nvelho\n<!-- tuning:end -->\nfim\n",
        encoding="utf-8",
    )
    arguments = ["--consensus", str(consensus), "--input-dir", str(gold_dir),
                 "--metrics", str(metrics), "--history", str(history)]

    assert tune_cfr.main(arguments) == 0
    payload = json.loads(metrics.read_text(encoding="utf-8"))
    # v1 erra v1.2.1 (patch sem fix) e perde v1.2.0; v2 herda esse FP de v1.
    # v3 com corte 1,25 exige patch + keyword ou só keywords (score 2): acerta tudo.
    assert payload["best"]["name"] == "v3 kw=base match=substring corte=1.25"
    assert payload["best"]["f1"] == 1.0
    assert payload["meets_target"] is True
    assert payload["items"] == 4
    assert payload["items_with_commits"] == 4

    text = history.read_text(encoding="utf-8")
    assert text.startswith("# Histórico\n\nTexto manual.")
    assert text.rstrip().endswith("fim")
    assert "velho" not in text
    assert "| v1 | 0.500 | 0.500 | 0.500 | 1 | 1 | 1 | 1 |" in text


def test_main_without_consensus_fails(tmp_path: Path, capsys) -> None:
    assert tune_cfr.main(["--consensus", str(tmp_path / "missing.csv")]) == 2
    assert "agreement.py" in capsys.readouterr().err
