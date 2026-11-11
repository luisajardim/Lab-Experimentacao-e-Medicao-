"""Testes da Seção 7 — conclusão e seletor de α (T12, #87)."""

import sys

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

import simulate
from config import ALPHAS, ROOT

sys.path.insert(0, str(ROOT))
import app  # noqa: E402, I001


@pytest.mark.parametrize("alpha", ALPHAS)
def test_expectation_table_uses_simulated_rates_for_alpha(alpha):
    summary = simulate.load_summary()
    table = app.expectation_table(summary, alpha)
    assert list(table.columns) == [
        "Pergunta",
        "O grupo esperava (31/10)",
        "Simulação (Pearson / Spearman)",
        "Confirmou?",
    ]
    assert len(table) == 5
    p = app._rate(summary, "S-real", 0.6, "pearson", alpha)
    s = app._rate(summary, "S-real", 0.6, "spearman", alpha)
    row = table[table["Pergunta"].str.startswith("Q3 — Poder na S-real (")].iloc[0]
    assert row["Simulação (Pearson / Spearman)"] == f"{app._pct(p)} / {app._pct(s)}"


def test_rate_reads_one_cell():
    summary = pd.DataFrame(
        {
            "situation": ["S-base", "S-base"],
            "rho": [0.1, 0.1],
            "test": ["pearson", "spearman"],
            "alpha": [0.05, 0.05],
            "reject_rate": [0.2, 0.3],
        }
    )
    assert app._rate(summary, "S-base", 0.1, "spearman", 0.05) == 0.3


def _section7_text(at: AppTest) -> str:
    return "\n".join(m.value for m in at.markdown)


def test_section7_has_required_blocks_and_reacts_to_alpha():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120)
    at.run()
    assert not at.exception
    subheaders = [s.value for s in at.subheader]
    for block in (
        "O que esperávamos × o que encontramos",
        "Resposta à pergunta",
        "Recomendação",
        "Principal limitação",
    ):
        assert block in subheaders
    text_05 = _section7_text(at)
    assert "Spearman" in text_05 and "mudaria para o Pearson" in text_05

    at.selectbox[0].set_value(0.01).run()
    assert not at.exception
    assert _section7_text(at) != text_05  # números da S-outlier/S-real mudam com α

