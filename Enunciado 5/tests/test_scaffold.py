"""Testes de fumaça do scaffold (T01, #96)."""

import importlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = ["config", "schema", "synthetic", "cli"]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports_and_has_docstring(name):
    module = importlib.import_module(name)
    assert module.__doc__ and module.__doc__.strip()


@pytest.mark.parametrize("path", ["src", "tests", "docs/schema.md", "app.py", "PLAN.md",
                                  "data/raw/synthetic/runs.csv"])
def test_project_layout(path):
    assert (ROOT / path).exists()


def test_config_consistency():
    import config

    assert config.CONTROL in config.MANAGERS
    assert set(config.PALETTE) == set(config.MANAGERS)
    assert config.YARN_VARIANTS == ("yarn-classic", "yarn-berry-nm", "yarn-berry-pnp")
    assert len(config.MANAGERS) == 6 and len(config.SCENARIOS) == 4 and len(config.PROJECTS) == 3


def test_cli_unknown_subcommand_returns_error():
    import cli

    assert cli.main(["nao-existe"]) == 2


def test_cli_prepare_only(monkeypatch):
    import cli

    called = []
    monkeypatch.setattr(cli, "prepare_pipeline", lambda: called.append(True))
    assert cli.main(["--prepare-only"]) == 0
    assert called
