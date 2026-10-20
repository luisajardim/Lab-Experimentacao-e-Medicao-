from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import sys


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "generate_gold.py"
SPEC = importlib.util.spec_from_file_location("generate_gold", SCRIPT_PATH)
assert SPEC and SPEC.loader
generate_gold = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generate_gold
SPEC.loader.exec_module(generate_gold)


def _repository_payload(name: str, release_count: int = 5) -> dict[str, object]:
    return {
        "repository": {"full_name": name},
        "releases": [
            {
                "draft": False,
                "prerelease": False,
                "published_at": f"2026-01-{index + 1:02d}T00:00:00Z",
                "html_url": f"https://github.com/{name}/releases/tag/v{index}",
            }
            for index in range(release_count)
        ],
    }


def test_main_generates_reproducible_template_from_multiple_input_directories(
    tmp_path: Path,
) -> None:
    first_input = tmp_path / "first"
    second_input = tmp_path / "second" / "nested"
    first_input.mkdir(parents=True)
    second_input.mkdir(parents=True)

    (first_input / "owner-one").mkdir()
    (first_input / "owner-one" / "one.json").write_text(
        json.dumps(_repository_payload("org/one")), encoding="utf-8"
    )
    (second_input / "two.json").write_text(
        json.dumps(_repository_payload("org/two", release_count=6)), encoding="utf-8"
    )
    # A repo without five usable releases must not enter the sample.
    (first_input / "owner-excluded").mkdir()
    (first_input / "owner-excluded" / "excluded.json").write_text(
        json.dumps(_repository_payload("org/excluded", release_count=4)), encoding="utf-8"
    )
    # Files at the root are generated gold artifacts and must be ignored.
    (first_input / "llm_suggestions.json").write_text("[]", encoding="utf-8")

    output = tmp_path / "gold" / "template.csv"
    population = tmp_path / "datasets" / "metrics.csv"
    population.parent.mkdir()
    population.write_text("full_name\norg/one\norg/two\n", encoding="utf-8")
    arguments = [
        "--input-dir",
        str(first_input),
        "--input-dir",
        str(tmp_path / "second"),
        "--output",
        str(output),
        "--population-csv",
        str(population),
        "--sample-size",
        "2",
    ]

    assert generate_gold.main(arguments) == 0
    first_run = output.read_bytes()
    assert generate_gold.main(arguments) == 0
    assert output.read_bytes() == first_run

    with output.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 2
    assert tuple(rows[0]) == generate_gold.OUTPUT_COLUMNS
    assert {row["full_name"] for row in rows} == {"org/one", "org/two"}
    assert all(row["project_type"] == "" for row in rows)
    assert all(row["delivers_to_user"] == "" for row in rows)
    assert all(row["notes"] == "" for row in rows)
    assert all(row["release_url_1"].startswith("https://github.com/") for row in rows)
