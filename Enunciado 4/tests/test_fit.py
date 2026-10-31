"""Testes do ajuste dos parâmetros da simulação (T03, #77)."""

import json

import numpy as np
import pandas as pd
import pytest

from config import SEED
from data import FULL_CSV
from fit import PARAMS_JSON, fit_gamma, fit_nbinom, fit_params


def test_fit_gamma_recovers_known_parameters():
    rng = np.random.default_rng(SEED)
    x = rng.gamma(shape=0.6, scale=500, size=20_000)
    par = fit_gamma(x)
    assert par["shape"] == pytest.approx(0.6, rel=0.03)
    assert par["scale"] == pytest.approx(500, rel=0.05)


def test_fit_nbinom_recovers_known_parameters():
    rng = np.random.default_rng(SEED)
    r, mean = 0.2, 5.0
    y = rng.negative_binomial(r, r / (r + mean), size=20_000)
    par = fit_nbinom(y)
    assert par["r"] == pytest.approx(r, rel=0.05)
    assert par["mean"] == pytest.approx(mean, rel=0.05)
    assert par["p"] == pytest.approx(par["r"] / (par["r"] + par["mean"]))


def test_committed_params_match_regeneration():
    committed = json.loads(PARAMS_JSON.read_text())
    fresh = fit_params(pd.read_csv(FULL_CSV))
    for block in ("loc", "defects", "observed"):
        for key, value in committed[block].items():
            if isinstance(value, float):
                assert fresh[block][key] == pytest.approx(value, rel=1e-6), (block, key)
    assert committed["base"] == fresh["base"]


def test_kc1_fit_is_reasonable():
    par = json.loads(PARAMS_JSON.read_text())
    assert par["loc"]["ks_pvalue"] > 0.05
    assert abs(par["defects"]["p_zero_fit"] - par["defects"]["p_zero_obs"]) < 0.05
