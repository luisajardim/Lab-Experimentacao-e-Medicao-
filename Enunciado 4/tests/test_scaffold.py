"""Testes de fumaça do scaffold (T01, #75).

Garantem que a estrutura do projeto existe e que cada módulo de `src/`
importa e está documentado.
"""

import importlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = ["config", "data", "fit", "generate", "stat_tests", "simulate", "figures", "cli", "relatorio"]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports_and_has_docstring(name):
    module = importlib.import_module(name)
    assert module.__doc__ and module.__doc__.strip()


@pytest.mark.parametrize("path", ["data/real", "data/sim", "docs", "app.py"])
def test_project_layout(path):
    assert (ROOT / path).exists()
