"""Testes dos gráficos G1 (T06a, #80) e G2 (T06b, #81)."""

from dataclasses import replace

import numpy as np
import plotly.graph_objects as go
import pytest
from scipy import stats

import stat_tests
from config import COLOR_PEARSON, COLOR_SPEARMAN
from figures import G1_TEXT, G2_TEXT, _null_density, _null_t, fig_g1, fig_g2

G2_REPS = 2000


def test_fig_g1_returns_plotly_figure_with_traces():
    fig = fig_g1()
    assert isinstance(fig, go.Figure)
    # 4 séries × 2 painéis (LOC e defeitos) = 8 traces de histograma
    assert len(fig.data) == 8
    trace_names = {t.name for t in fig.data}
    assert any("Amostra (n = 30)" in name for name in trace_names)
    assert any("KC1 completo" in name for name in trace_names)
    assert any("S-real" in name for name in trace_names)


def test_fig_g1_has_title_units_and_legend():
    fig = fig_g1()
    assert fig.layout.title.text and "G1" in fig.layout.title.text
    assert "LOC" in fig.layout.xaxis.title.text
    assert "linhas de código" in fig.layout.xaxis.title.text
    assert "defeitos" in fig.layout.xaxis2.title.text.lower()
    assert "%" in fig.layout.yaxis.title.text
    assert any(t.showlegend for t in fig.data)


def test_fig_g1_is_reproducible_with_seed():
    f1 = fig_g1(seed=42)
    f2 = fig_g1(seed=42)
    for t1, t2 in zip(f1.data, f2.data, strict=True):
        np.testing.assert_array_equal(t1.x, t2.x)


def test_g1_text_covers_shape_and_distributions():
    sentences = [s.strip() for s in G1_TEXT.split(".") if s.strip()]
    # Texto curto de 2 a 4 frases (cuidado com decimais com vírgula em português)
    assert 2 <= len(sentences) <= 4
    lower = G1_TEXT.lower()
    for term in ("assimetria", "zero", "gamma", "binomial negativa"):
        assert term in lower


def _trace(fig, prefix, axis="x"):
    return next(t for t in fig.data if (t.name or "").startswith(prefix) and t.xaxis == axis)


def _points(values):
    return np.array([v for v in values if v is not None], dtype=float)


def _polygon_area(xs, ys):
    """Área dos polígonos separados por None (fórmula do cadarço)."""
    total, part = 0.0, []
    for x, y in [*zip(xs, ys, strict=True), (None, None)]:
        if x is None:
            px, py = np.array(part).T
            total += abs(np.dot(px, np.roll(py, 1)) - np.dot(py, np.roll(px, 1))) / 2
            part = []
        else:
            part.append((x, y))
    return total


def test_fig_g2_has_every_element_per_panel_with_fixed_colors():
    fig = fig_g2(reps=G2_REPS)
    assert isinstance(fig, go.Figure)
    assert _trace(fig, "Nula simulada — Pearson", "x").marker.color == COLOR_PEARSON
    assert _trace(fig, "Nula simulada — Spearman", "x2").marker.color == COLOR_SPEARMAN
    assert _trace(fig, "p-valor do exemplo — Pearson", "x").fillcolor == COLOR_PEARSON
    assert _trace(fig, "p-valor do exemplo — Spearman", "x2").fillcolor == COLOR_SPEARMAN
    for axis in ("x", "x2"):
        assert _trace(fig, "Curva teórica t(28)", axis)
        assert _trace(fig, "Região de rejeição", axis)


def test_fig_g2_has_title_axes_and_legend_without_repeated_items():
    fig = fig_g2(reps=G2_REPS)
    assert "G2" in fig.layout.title.text
    assert "Estatística t" in fig.layout.xaxis.title.text
    assert "Estatística t" in fig.layout.xaxis2.title.text
    assert "Densidade" in fig.layout.yaxis.title.text
    names = [t.name for t in fig.data if t.showlegend is not False]
    assert len(names) == len(set(names)) == 6


@pytest.mark.parametrize("alpha", [0.05, 0.01])
def test_rejection_region_starts_at_critical_t_of_alpha(alpha):
    fig = fig_g2(alpha=alpha, reps=G2_REPS)
    region = np.abs(_points(_trace(fig, "Região de rejeição").x))
    assert region.min() == pytest.approx(stats.t.ppf(1 - alpha / 2, 28))
    assert region.max() == 5.0


def test_shaded_area_is_the_p_value_of_the_example():
    example = stat_tests.run_example()
    fig = fig_g2(example=example, reps=G2_REPS)
    for name, axis, result in (
        ("Pearson", "x", example.pearson),
        ("Spearman", "x2", example.spearman),
    ):
        area = _trace(fig, f"p-valor do exemplo — {name}", axis)
        assert np.abs(_points(area.x)).min() == pytest.approx(abs(result.t))
        # A área vai só até |t| = 5; além disso a cauda de t(28) é desprezível.
        assert _polygon_area(area.x, area.y) == pytest.approx(result.p, abs=1e-3)


def test_g2_omits_p_area_when_observed_t_is_outside_the_axis():
    example = stat_tests.run_example()
    perfect = stat_tests.pearson([1, 2, 3, 4], [1, 2, 3, 4])._replace(df=28)
    fig = fig_g2(example=replace(example, pearson=perfect), reps=G2_REPS)
    assert not any((t.name or "") == "p-valor do exemplo — Pearson" for t in fig.data)
    assert _trace(fig, "p-valor do exemplo — Spearman", "x2")


def test_null_density_keeps_values_outside_the_axis_in_the_denominator():
    _, density = _null_density(np.array([0.1, 0.1, 100.0, -100.0]))
    assert density.sum() * 0.25 == pytest.approx(0.5)


def test_null_has_mean_near_zero_and_rejection_near_alpha():
    critical = stats.t.ppf(0.975, 28)
    for t in _null_t(G2_REPS, 43):
        assert abs(t.mean()) < 0.1
        assert 0.03 < np.mean(np.abs(t) > critical) < 0.08


def test_text_claims_about_the_shape_of_each_null():
    critical = stats.t.ppf(0.975, 28)
    pearson_t, spearman_t = _null_t(G2_REPS, 43)
    # Spearman acompanha a curva: simétrico e com rejeição parecida nas duas caudas.
    assert abs(stats.skew(spearman_t)) < 0.2
    assert np.mean(spearman_t > critical) < 2 * np.mean(spearman_t < -critical)
    # Pearson: mais pontudo, cauda direita longa e rejeições quase só à direita.
    assert stats.kurtosis(pearson_t) > stats.kurtosis(spearman_t) + 1
    assert stats.skew(pearson_t) > 1
    assert np.mean(pearson_t > critical) > 5 * np.mean(pearson_t < -critical)


def test_g2_text_mentions_right_tail_of_pearson():
    assert "cauda direita" in G2_TEXT


def test_fig_g2_is_reproducible():
    first, second = fig_g2(reps=G2_REPS, seed=7), fig_g2(reps=G2_REPS, seed=7)
    np.testing.assert_array_equal(
        _trace(first, "Nula simulada — Pearson").y, _trace(second, "Nula simulada — Pearson").y
    )


def test_g2_text_covers_required_points():
    lower = G2_TEXT.lower()
    for term in ("pearson", "spearman", "postos", "região de rejeição", "bicaudal", "crítico"):
        assert term in lower
    assert "se $h_0$ fosse verdadeira" in lower
    assert "não é a probabilidade de $h_0$ ser verdadeira" in lower

