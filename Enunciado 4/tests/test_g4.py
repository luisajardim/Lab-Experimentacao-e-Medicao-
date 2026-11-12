"""Testes do gráfico G4 — curvas de poder (T10, #85)."""

import numpy as np
import plotly.graph_objects as go
import pytest

import simulate
from config import COLOR_PEARSON, COLOR_SPEARMAN, EFFECT_GRID, SITUATIONS
from figures import G4_TEXT, fig_g4


def _curves(fig: go.Figure, name: str) -> list[go.Scatter]:
    return [t for t in fig.data if t.name == name]


def test_fig_g4_has_one_panel_per_situation_with_both_tests():
    fig = fig_g4()
    assert isinstance(fig, go.Figure)
    titles = [a.text for a in fig.layout.annotations]
    for situation in SITUATIONS:
        assert any(title.startswith(situation) for title in titles)
    assert len(_curves(fig, "Pearson")) == len(SITUATIONS)
    assert len(_curves(fig, "Spearman")) == len(SITUATIONS)


def test_fig_g4_uses_fixed_colors_and_at_least_five_effects_from_zero():
    fig = fig_g4()
    for name, color in (("Pearson", COLOR_PEARSON), ("Spearman", COLOR_SPEARMAN)):
        for trace in _curves(fig, name):
            assert trace.line.color == color
            assert len(trace.x) >= 5 and trace.x[0] == 0.0
    # cada teste aparece uma vez só na legenda
    assert sum(bool(t.showlegend) for t in _curves(fig, "Pearson")) == 1


@pytest.mark.parametrize("alpha", [0.05, 0.01])
def test_fig_g4_matches_simulation_summary(alpha):
    summary = simulate.load_summary()
    fig = fig_g4(alpha=alpha)
    expected = summary[
        np.isclose(summary["alpha"], alpha)
        & (summary["situation"] == "S-real")
        & (summary["test"] == "spearman")
    ].sort_values("rho")
    trace = _curves(fig, "Spearman")[list(SITUATIONS).index("S-real")]
    np.testing.assert_allclose(trace.y, expected["reject_rate"])
    assert f"{alpha:.2f}".replace(".", ",") in fig.layout.title.text


def test_fig_g4_alpha_changes_the_curves_and_reference_line():
    f05, f01 = fig_g4(alpha=0.05), fig_g4(alpha=0.01)
    p05 = np.array(_curves(f05, "Pearson")[0].y)
    p01 = np.array(_curves(f01, "Pearson")[0].y)
    assert (p01 <= p05).all() and (p01 < p05).any()
    line05 = next(t for t in f05.data if t.name and t.name.startswith("α ="))
    assert line05.y[0] == pytest.approx(0.05)


def test_fig_g4_has_title_axes_and_population_annotations():
    fig = fig_g4()
    assert fig.layout.title.text.startswith("G4")
    assert "%" in fig.layout.yaxis.title.text
    assert "ρ latente" in fig.layout.xaxis.title.text
    ticks = fig.layout.xaxis.ticktext
    assert len(ticks) == len(EFFECT_GRID)
    assert all("r=" in t and "ρₛ=" in t for t in ticks)


def test_fig_g4_rejects_unknown_alpha():
    with pytest.raises(ValueError):
        fig_g4(alpha=0.10)


def test_g4_text_is_short_and_covers_required_points():
    sentences = [s for s in G4_TEXT.replace("0,", "0_").split(". ") if s.strip()]
    assert 2 <= len(sentences) <= 4
    for term in ("S-base", "S-real", "n = 10", "S-outlier", "Spearman", "Pearson"):
        assert term in G4_TEXT


def test_fig_g4_can_put_every_situation_in_one_row():
    fig = fig_g4(0.05, cols=len(SITUATIONS))
    domains = {fig.layout[f"yaxis{i if i > 1 else ''}"].domain for i in range(1, len(SITUATIONS) + 1)}
    assert len(domains) == 1  # todos os painéis na mesma altura
