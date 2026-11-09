"""Testes do extra de tamanho da amostra (T14, #91)."""

import json
import shutil

import numpy as np
import pandas as pd
import pytest

import cli
import sample_size
from config import ALPHAS, DATA_SIM, REPS
from sample_size import (
    calibrate_latent_rho,
    config_snapshot,
    n80_table,
    n_for_power,
    observed_rho_s,
    run,
    summary_text,
)
from simulate import POPULATION_FILE, cache_key


def _curve(powers, ns=(10, 20, 30, 50)):
    return pd.DataFrame({"n": ns, "reject_rate": powers})


def test_n_for_power_interpolates_in_log_n():
    n = n_for_power(_curve([0.2, 0.5, 0.7, 0.9]))
    assert 30 < n < 50
    expected = np.exp(np.log(30) + 0.5 * (np.log(50) - np.log(30)))
    assert n == pytest.approx(expected)


def test_n_for_power_edges():
    assert n_for_power(_curve([0.85, 0.9, 0.95, 0.99])) == 10
    assert np.isnan(n_for_power(_curve([0.1, 0.2, 0.3, 0.4])))


def test_calibrate_latent_rho():
    pop = pd.DataFrame({"situation": "S-real", "rho": [0.0, 0.3, 0.6], "rho_s_pop": [0.0, 0.25, 0.5]})
    assert calibrate_latent_rho("S-real", 0.375, pop) == pytest.approx(0.45)
    with pytest.raises(ValueError):
        calibrate_latent_rho("S-real", 0.9, pop)


@pytest.fixture(scope="module")
def small_run(tmp_path_factory):
    out = tmp_path_factory.mktemp("ss")
    shutil.copy(DATA_SIM / POPULATION_FILE, out / POPULATION_FILE)
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sample_size, "N_GRID", (10, 30))
        results = run(reps=200, out_dir=out, verbose=False)
    return out, results


def test_small_run_shape(small_run):
    _, results = small_run
    assert len(results) == 2 * 3 * 2 * 2 * len(ALPHAS)  # situações × efeitos × n × testes × α
    assert set(results["effect"]) == {"zero", "moderado", "observado"}


def test_small_run_uses_cache(small_run, monkeypatch):
    out, _ = small_run
    calls = []
    monkeypatch.setattr(sample_size, "N_GRID", (10, 30))
    monkeypatch.setattr(sample_size, "simulate_n_cell", lambda *a, **k: calls.append(a))
    run(reps=200, out_dir=out, verbose=False)
    assert calls == []


def test_committed_results_are_current():
    meta = json.loads((DATA_SIM / sample_size.META_FILE).read_text())
    assert meta["cache_key"] == cache_key(config_snapshot(REPS, observed_rho_s()))
    results = sample_size.load()
    table = n80_table(results).set_index(["situation", "effect", "test"]).sort_index()
    # Com o efeito observado, o Spearman precisa de menos classes que o Pearson para 80% de poder.
    obs = table.loc[("S-real", "observado")]
    assert obs.loc["spearman", "n80"] < obs.loc["pearson", "n80"]


def test_summary_text_is_short_and_in_portuguese_format():
    text = summary_text(sample_size.load())
    sentences = [s for s in text.split(". ") if s.strip()]
    assert 2 <= len(sentences) <= 4
    assert "0,5" in text and "0.5" not in text


def test_cli_flag_runs_extra_and_is_not_passed_to_streamlit(monkeypatch):
    calls = []
    monkeypatch.setattr(sample_size, "main", lambda argv=None: calls.append(argv))
    monkeypatch.setattr(cli.subprocess, "run", lambda *a, **k: pytest.fail("não deveria abrir o Streamlit"))
    assert cli.main(["--prepare-only", "--sample-size"]) == 0
    assert calls == [[]]
