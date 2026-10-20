#!/usr/bin/env python3
"""Create a reproducible candidate manifest from search results or local gold JSONs."""

import argparse
import csv
import json
import random
import tomllib
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/candidates.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/raw/candidate_manifest.csv"))
    parser.add_argument(
        "--size",
        type=int,
        help="Tamanho do corte aleatório; omitido com --from-gold preserva todos os elegíveis.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--from-gold",
        action="store_true",
        help="Monta o manifesto com todos os JSONs locais que passam os filtros oficiais.",
    )
    parser.add_argument("--config", type=Path, default=Path("config.toml"))
    args = parser.parse_args()

    if args.from_gold:
        with args.config.open("rb") as file:
            config = tomllib.load(file)
        root = args.config.parent
        gold_dir = root / config["paths"]["gold_dir"]
        start, end = config["window"]["start"], config["window"]["end"]
        minimum_releases = config["filters"]["min_releases"]
        minimum_runs = config["filters"]["min_workflow_runs"]
        selected = []
        for path in gold_dir.rglob("*.json"):
            if path.parent == gold_dir:
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            repository = payload.get("repository", {})
            name, branch = repository.get("full_name"), repository.get("default_branch")
            if not isinstance(name, str) or not isinstance(branch, str):
                continue
            releases = [
                release
                for release in payload.get("releases", [])
                if start <= str(release.get("published_at", ""))[:10] <= end
                and not release.get("draft", False)
                and not release.get("prerelease", False)
            ]
            runs = [
                run
                for month in payload.get("runs_by_month", {}).values()
                for run in month
                if run.get("branch") == branch and run.get("event") == "push"
            ]
            if len(releases) >= minimum_releases and len(runs) >= minimum_runs:
                selected.append(
                    {
                        "full_name": name,
                        "stars": repository.get("stars", ""),
                        "language": repository.get("language", ""),
                        "default_branch": branch,
                        "created_at": repository.get("created_at", ""),
                    }
                )
    else:
        with args.input.open(encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        size = args.size or 2000
        if len(rows) < size:
            raise ValueError(f"need {size} candidates, found {len(rows)}")
        selected = random.Random(args.seed).sample(rows, size)

    if args.size is not None:
        if args.size <= 0:
            raise ValueError("size must be greater than zero")
        if len(selected) < args.size:
            raise ValueError(f"need {args.size} eligible candidates, found {len(selected)}")
        selected = random.Random(args.seed).sample(selected, args.size)

    selected.sort(key=lambda row: row["full_name"].casefold())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["full_name", "stars", "language", "default_branch", "created_at"],
        )
        writer.writeheader()
        writer.writerows(selected)
    print(f"Manifesto gerado: {len(selected)} repositórios em {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
