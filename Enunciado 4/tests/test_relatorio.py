"""Testes da página "Relatório" e da navegação entre as páginas (#93).

O Relatório é o formato que o enunciado avalia (§4): 7 seções na ordem, links no
topo e um texto curto (2 a 4 frases) junto de cada gráfico. O Dashboard (painel só
com gráficos) é testado em `test_app_and_cli.py`.
"""

import re
import sys

import pytest
from streamlit.testing.v1 import AppTest

import relatorio
from config import DASHBOARD_URL, PROJECTS_URL, REPO_URL, ROOT

sys.path.insert(0, str(ROOT))
import app  # noqa: E402, I001

SECTIONS = [
    "1. Cenário",
    "2. Os dados (G1)",
    "3. Como os testes funcionam (G2)",
    "4. Erro tipo I (G3)",
    "5. Poder (G4)",
    "6. Dados reais",
    "7. Conclusão",
]

SCRIPT = f"""
import sys
sys.path.insert(0, {str(ROOT / "src")!r})
import streamlit as st
import relatorio
st.session_state.setdefault(relatorio.SHARED_ALPHA, {{alpha}})
relatorio.main()
"""


def _render(alpha: float = 0.05) -> AppTest:
    at = AppTest.from_string(SCRIPT.replace("{alpha}", repr(alpha)), default_timeout=180)
    at.run()
    assert not at.exception
    return at


@pytest.fixture(scope="module")
def report() -> AppTest:
    return _render()


def _sentences(text: str) -> int:
    text = re.sub(r"\$[^$]*\$", "X", text.replace("**", ""))
    return len([s for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ(])", text.strip()) if s])


def test_report_has_the_seven_sections_in_order(report):
    headers = [h.value for h in report.header]
    assert headers[: len(SECTIONS)] == SECTIONS
    assert headers[len(SECTIONS):] in ([], ["Para discutir: tamanho da amostra"])


def test_report_has_the_required_links_at_the_top(report):
    links = next(m.value for m in report.markdown if "Links do Projeto" in m.value)
    for url in (DASHBOARD_URL, REPO_URL, PROJECTS_URL):
        assert url in links


def test_report_shows_charts_and_the_real_data_table(report):
    assert len(report.get("plotly_chart")) >= 4  # G1 a G4 (+ extra)
    assert len(report.dataframe) >= 1


@pytest.mark.parametrize("alpha", [0.05, 0.01])
def test_g3_summary_has_two_to_four_sentences(alpha):
    assert 2 <= _sentences(relatorio.g3_summary(alpha)) <= 4


def test_report_opens_with_the_alpha_chosen_on_the_dashboard():
    at = _render(alpha=0.01)
    assert at.selectbox(key="alpha_relatorio").value == 0.01


def test_dashboard_url_points_to_the_published_app():
    assert DASHBOARD_URL == "https://experimentacao-lab04-spearman.streamlit.app"
    assert "lab-experimentacao-medicao-lab04" not in DASHBOARD_URL


def test_router_opens_the_dashboard_with_links_to_everything():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=180)
    at.run()
    assert not at.exception
    caption = " ".join(c.value for c in at.caption)
    for url in (DASHBOARD_URL, REPO_URL, PROJECTS_URL):
        assert url in caption
    assert callable(app.dashboard_page) and callable(relatorio.main)
