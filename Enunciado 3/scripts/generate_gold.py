#!/usr/bin/env python3
"""Generate the reproducible CSV template used for manual gold labeling.

Input contract
--------------
``--input-dir`` may be supplied more than once.  Every ``*.json`` file below
each *subdirectory* of a supplied directory is interpreted as one repository
record (directories are searched recursively).  JSON files placed directly in
an input directory are ignored: ``data/gold`` also holds generated artifacts
such as labels, audits, and LLM suggestions.  Each record must contain:

* ``repository.full_name``: the GitHub repository identifier (``owner/name``);
* ``releases``: a list of release objects.  A release eligible for labeling
  has ``draft != true``, ``prerelease != true`` and a non-empty ``html_url``.

Only repositories with at least five eligible releases can enter the sample.
The same ``full_name`` in two files is rejected, rather than silently biasing
the draw.

Output contract
---------------
The script writes one UTF-8 CSV row per sampled repository.  Its columns are
``full_name``, ``project_type``, ``delivers_to_user``, ``release_url_1`` to
``release_url_5``, and ``notes``.  The annotation columns start empty; the
release URLs are complete GitHub URLs and therefore usable as clickable links
by spreadsheet applications.  The CSV contains exactly ``--sample-size``
rows, or the command fails before writing when there are too few eligible
repositories.

Examples
--------
    python scripts/generate_gold.py
    python scripts/generate_gold.py --input-dir data/raw --input-dir data/gold \\
        --output-dir data/gold
    python scripts/generate_gold.py --output data/gold/labels_template.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Change these two constants when the team settles the canonical locations.
DEFAULT_INPUT_DIRS = (PROJECT_ROOT / "data" / "gold",)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "gold"
DEFAULT_OUTPUT_FILENAME = "labels_template.csv"
DEFAULT_SAMPLE_SIZE = 60
DEFAULT_RANDOM_STATE = 42

OUTPUT_COLUMNS = (
    "full_name",
    "project_type",
    "delivers_to_user",
    "release_url_1",
    "release_url_2",
    "release_url_3",
    "release_url_4",
    "release_url_5",
    "notes",
)


@dataclass(frozen=True)
class RepositoryForLabeling:
    full_name: str
    releases: tuple[dict[str, Any], ...]


def _eligible_releases(releases: object) -> tuple[dict[str, Any], ...]:
    if not isinstance(releases, list):
        raise ValueError("'releases' must be a list")

    eligible = [
        release
        for release in releases
        if isinstance(release, dict)
        and not release.get("draft", False)
        and not release.get("prerelease", False)
        and isinstance(release.get("html_url"), str)
        and release["html_url"].strip()
    ]
    return tuple(eligible)


def load_repositories(input_dirs: Iterable[Path]) -> list[RepositoryForLabeling]:
    """Load repository records from JSON files inside input subdirectories.

    Files directly in an input directory are derived gold artifacts, not raw
    repository records, so they must not influence the sample.
    """
    files: list[Path] = []
    for input_dir in input_dirs:
        if not input_dir.is_dir():
            raise ValueError(f"input directory does not exist or is not a directory: {input_dir}")
        files.extend(path for path in input_dir.rglob("*.json") if path.parent != input_dir)

    repositories: list[RepositoryForLabeling] = []
    seen_full_names: dict[str, Path] = {}
    for path in sorted(files):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid JSON in {path}: {error.msg}") from error

        if not isinstance(payload, dict) or not isinstance(payload.get("repository"), dict):
            raise ValueError(f"{path}: missing object 'repository'")
        full_name = payload["repository"].get("full_name")
        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError(f"{path}: missing non-empty 'repository.full_name'")
        full_name = full_name.strip()

        if full_name in seen_full_names:
            raise ValueError(
                f"duplicate repository '{full_name}' in {path} and {seen_full_names[full_name]}"
            )
        seen_full_names[full_name] = path

        releases = _eligible_releases(payload.get("releases"))
        if len(releases) >= 5:
            repositories.append(RepositoryForLabeling(full_name, releases))

    return repositories


def select_repositories(
    repositories: Sequence[RepositoryForLabeling], sample_size: int, random_state: int
) -> list[RepositoryForLabeling]:
    """Return a stable, seed-controlled sample sorted by repository name."""
    if sample_size <= 0:
        raise ValueError("sample size must be greater than zero")
    ordered = sorted(repositories, key=lambda repository: repository.full_name.casefold())
    if len(ordered) < sample_size:
        raise ValueError(
            f"need {sample_size} eligible repositories, but only found {len(ordered)}"
        )
    return sorted(
        random.Random(random_state).sample(ordered, sample_size),
        key=lambda repository: repository.full_name.casefold(),
    )


def _release_urls(repository: RepositoryForLabeling, random_state: int) -> list[str]:
    """Draw five releases deterministically, preserving chronological display order."""
    generator = random.Random(f"{random_state}:{repository.full_name}")
    chosen = generator.sample(list(repository.releases), 5)
    chosen.sort(key=lambda release: str(release.get("published_at", "")))
    return [str(release["html_url"]).strip() for release in chosen]


def build_rows(
    repositories: Iterable[RepositoryForLabeling], random_state: int
) -> list[dict[str, str]]:
    """Create empty labeling rows and five deterministically selected release links."""
    rows: list[dict[str, str]] = []
    for repository in repositories:
        release_urls = _release_urls(repository, random_state)
        row = {
            "full_name": repository.full_name,
            "project_type": "",
            "delivers_to_user": "",
            "notes": "",
        }
        row.update(
            {f"release_url_{index}": url for index, url in enumerate(release_urls, start=1)}
        )
        rows.append(row)
    return rows


def write_csv(rows: Iterable[dict[str, str]], output_path: Path) -> None:
    """Write the gold template, creating the chosen output directory if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        action="append",
        type=Path,
        metavar="DIR",
        help="Directory containing repository JSON files; repeat to combine directories.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for the CSV (default: {DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Explicit output CSV path; takes precedence over --output-dir.",
    )
    parser.add_argument(
        "--population-csv",
        type=Path,
        metavar="CSV",
        help="Restrict the draw to full_name values in the final metrics CSV.",
    )
    parser.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE_SIZE)
    parser.add_argument("--random-state", type=int, default=DEFAULT_RANDOM_STATE)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    input_dirs = tuple(args.input_dir) if args.input_dir else DEFAULT_INPUT_DIRS
    output_path = args.output or args.output_dir / DEFAULT_OUTPUT_FILENAME

    try:
        repositories = load_repositories(input_dirs)
        if args.population_csv:
            with args.population_csv.open(encoding="utf-8-sig", newline="") as file:
                population = {row["full_name"].strip() for row in csv.DictReader(file) if row.get("full_name")}
            repositories = [repository for repository in repositories if repository.full_name in population]
        sample = select_repositories(repositories, args.sample_size, args.random_state)
        write_csv(build_rows(sample, args.random_state), output_path)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"Generated {len(sample)} rows at {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
