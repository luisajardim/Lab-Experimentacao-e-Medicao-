"""Testes de fumaça do scaffold (T01).

Garantem que a CLI responde e que o `config.toml` respeita as
definições operacionais fixas do ENUNCIADO §3 (janela e filtros).
"""

import tomllib
from pathlib import Path

from pipeline.cli import build_parser

ROOT = Path(__file__).resolve().parents[1]


def test_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["--config", "config.toml", "--stage", "collect"])
    assert args.command is None
    assert args.stage == "collect"
    assert args.config == "config.toml"
    assert args.limit is None


def test_parser_limit_flag():
    parser = build_parser()
    args = parser.parse_args(["--limit", "2", "--stage", "collect"])
    assert args.limit == 2


def test_parser_doctor_subcommand():
    parser = build_parser()
    args = parser.parse_args(["doctor"])
    assert args.command == "doctor"


def test_config_window_matches_enunciado():
    config = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))
    assert config["window"]["start"] == "2025-10-01"
    assert config["window"]["end"] == "2026-09-30"
    assert config["window"]["weeks"] == 52.1


def test_config_inclusion_filters():
    config = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))
    assert config["filters"]["min_releases"] == 5
    assert config["filters"]["min_workflow_runs"] == 50
