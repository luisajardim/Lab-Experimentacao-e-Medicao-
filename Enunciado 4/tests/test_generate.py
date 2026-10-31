"""Testes do gerador de dados simulados (T04, #78)."""

import numpy as np
import pytest
from scipy import stats

from config import SEED, SITUATIONS
from generate import generate, load_params

BIG_N = 200_000


def rng(seed=SEED):
    return np.random.default_rng(seed)


@pytest.mark.parametrize("situation", list(SITUATIONS))
def test_shapes_follow_situation(situation):
    x, y = generate(situation, 0.3, reps=50, rng=rng())
    n = SITUATIONS[situation][1]
    assert x.shape == y.shape == (50, n)
    assert x.dtype == y.dtype == np.float64


def test_same_seed_same_data_and_different_seed_different_data():
    a = generate("S-real", 0.3, reps=100, rng=rng())
    b = generate("S-real", 0.3, reps=100, rng=rng())
    c = generate("S-real", 0.3, reps=100, rng=rng(SEED + 1))
    np.testing.assert_array_equal(a[0], b[0])
    np.testing.assert_array_equal(a[1], b[1])
    assert not np.array_equal(a[0], c[0])


@pytest.mark.parametrize("kind", ["base", "real"])
def test_rho_zero_gives_no_correlation(kind):
    x, y = generate(kind, 0.0, n=BIG_N, rng=rng())
    assert abs(stats.pearsonr(x[0], y[0])[0]) < 0.01
    assert abs(stats.spearmanr(x[0], y[0])[0]) < 0.01


def test_rho_zero_mean_sample_correlation_is_zero():
    x, y = generate("S-base", 0.0, reps=10_000, rng=rng())
    xc, yc = x - x.mean(axis=1, keepdims=True), y - y.mean(axis=1, keepdims=True)
    r = (xc * yc).sum(axis=1) / np.sqrt((xc**2).sum(axis=1) * (yc**2).sum(axis=1))
    assert abs(r.mean()) < 0.01


def test_base_is_standard_normal_with_target_correlation():
    x, y = generate("base", 0.5, n=BIG_N, rng=rng())
    assert np.corrcoef(x[0], y[0])[0, 1] == pytest.approx(0.5, abs=0.01)
    for v in (x[0], y[0]):
        assert v.mean() == pytest.approx(0, abs=0.01)
        assert v.std() == pytest.approx(1, abs=0.01)


def test_real_latent_correlation_matches_rho():
    x, y = generate("real", 0.4, n=BIG_N, rng=rng())
    scores = [stats.norm.ppf(stats.rankdata(v) / (BIG_N + 1)) for v in (x[0], y[0])]
    # os empates dos defeitos atenuam um pouco a correlação dos escores normais
    assert np.corrcoef(*scores)[0, 1] == pytest.approx(0.4, abs=0.05)


def test_real_marginals_match_fitted_parameters():
    par = load_params()
    x, y = generate("real", 0.3, n=BIG_N, rng=rng())
    x, y = x[0], y[0]
    # LOC inteiro e >= 1; quantis batem com a Gamma ajustada
    assert (x >= 1).all() and np.array_equal(x, np.round(x))
    gamma = stats.gamma(par["loc"]["shape"], scale=par["loc"]["scale"])
    for q in (0.25, 0.5, 0.75, 0.9):
        assert np.quantile(x, q) == pytest.approx(np.ceil(gamma.ppf(q)), rel=0.03)
    # defeitos: inteiros >= 0, proporção de zeros e média da binomial negativa
    assert (y >= 0).all() and np.array_equal(y, np.round(y))
    assert (y == 0).mean() == pytest.approx(par["defects"]["p_zero_fit"], abs=0.01)
    assert y.mean() == pytest.approx(par["defects"]["mean"], rel=0.03)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"situation": "S-real", "rho": 1.0},
        {"situation": "desconhecida", "rho": 0.3},
        {"situation": "real", "rho": 0.3},  # gerador sem n
    ],
)
def test_invalid_inputs_raise(kwargs):
    with pytest.raises(ValueError):
        generate(**kwargs, rng=rng())


def test_missing_rng_raises():
    with pytest.raises(ValueError):
        generate("S-real", 0.3)


def test_outlier_contamination_rate_and_tail():
    from config import OUTLIER_RATE, OUTLIER_TAIL

    par = load_params()
    x, y = generate("outlier", 0.0, n=BIG_N, rng=rng())
    x, y = x[0], y[0]
    x_cut = np.ceil(stats.gamma.ppf(OUTLIER_TAIL, par["loc"]["shape"], scale=par["loc"]["scale"]))
    y_cut = stats.nbinom.ppf(OUTLIER_TAIL, par["defects"]["r"], par["defects"]["p"])
    joint_tail = np.mean((x >= x_cut) & (y >= y_cut))
    # contaminação (1/145) + pares que caem nas duas caudas por acaso (~0,01 × 0,01)
    assert joint_tail == pytest.approx(OUTLIER_RATE + 1e-4, abs=0.001)
    assert (x >= 1).all() and np.array_equal(x, np.round(x))


def test_outlier_creates_association_for_pearson_only():
    x_real, y_real = generate("real", 0.0, n=BIG_N, rng=rng())
    x_out, y_out = generate("outlier", 0.0, n=BIG_N, rng=rng())
    assert stats.pearsonr(x_out[0], y_out[0])[0] > stats.pearsonr(x_real[0], y_real[0])[0] + 0.05
    assert abs(stats.spearmanr(x_out[0], y_out[0])[0]) < 0.03
