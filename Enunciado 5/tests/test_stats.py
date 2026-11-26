"""Testes da análise estatística (T08, #103), validados contra o scipy."""

import numpy as np
import pandas as pd
import pytest
from scipy import stats as sps

import stats
from config import CONTROL, MANAGERS, SEED, YARN_VARIANTS
from schema import load_runs


def _runs(effects: dict[str, float], reps: int = 10, machines=("a", "b", "c"),
          noise: float = 0.05, seed: int = SEED) -> pd.DataFrame:
    """Instalações artificiais: tempo = 10 s × fator do gerenciador × efeito da máquina × ruído."""
    rng = np.random.default_rng(seed)
    rows = []
    for m_i, machine in enumerate(machines):
        for rep in range(1, reps + 1):
            for manager, factor in effects.items():
                rows.append(
                    {
                        "machine": machine,
                        "project": "express-api",
                        "scenario": "cold",
                        "manager": manager,
                        "rep": rep,
                        "wall_s": 10 * factor * (1 + 0.3 * m_i) * rng.lognormal(0, noise),
                        "disk_mb": 100.0,
                        "cache_mb": 50.0,
                        "exit_code": 0,
                        "build_ok": True,
                    }
                )
    return pd.DataFrame(rows)


ALL_EQUAL = {m: 1.0 for m in MANAGERS}


# --------------------------------------------------------------------------- descritiva


def test_describe_uses_only_valid_runs_and_reports_valid_rate():
    df = _runs({"npm": 1.0, "pnpm": 0.5}, reps=4, machines=("a",))
    df.loc[df.index[-1], "build_ok"] = False   # última instalação do pnpm falhou
    df.loc[df.index[-1], "wall_s"] = 999.0
    out = stats.describe(df).set_index("manager")
    assert out.loc["pnpm", "n"] == 3
    assert out.loc["pnpm", "n_total"] == 4
    assert out.loc["pnpm", "valid_rate"] == pytest.approx(0.75)
    assert out.loc["pnpm", "median"] < 10   # o 999 s da falha não entra
    assert out.loc["npm", "iqr"] == pytest.approx(out.loc["npm", "q3"] - out.loc["npm", "q1"])


def test_describe_footprint_is_disk_plus_cache():
    out = stats.describe(_runs({"npm": 1.0}, reps=3), metric="footprint_mb")
    assert out["median"].iloc[0] == pytest.approx(150.0)


# --------------------------------------------------------------------------- tamanho do efeito


def test_cliffs_delta_extremes_and_known_value():
    assert stats.cliffs_delta([1, 2, 3], [4, 5, 6]) == -1.0
    assert stats.cliffs_delta([4, 5, 6], [1, 2, 3]) == 1.0
    assert stats.cliffs_delta([1, 2, 3], [1, 2, 3]) == 0.0
    # pares (x>y)=3, (x<y)=5, empates=1 em 9 pares -> δ = (3-5)/9
    assert stats.cliffs_delta([1, 3, 5], [2, 3, 6]) == pytest.approx(-2 / 9)


@pytest.mark.parametrize(
    ("delta", "label"),
    [(0.1, "desprezível"), (-0.2, "pequeno"), (0.4, "médio"), (-0.9, "grande")],
)
def test_cliff_magnitude(delta, label):
    assert stats.cliff_magnitude(delta) == label


def test_speedup_and_ci_contain_true_ratio():
    rng = np.random.default_rng(SEED)
    control = 10 * rng.lognormal(0, 0.05, 30)
    treatment = control / 2 * rng.lognormal(0, 0.05, 30)
    assert stats.speedup(control, treatment) == pytest.approx(2.0, rel=0.05)
    low, high = stats.speedup_ci(control, treatment)
    assert low < 2.0 < high
    assert stats.speedup_ci(control, treatment) == (low, high)   # semente fixa


# --------------------------------------------------------------------------- Holm


def test_holm_matches_manual_step_down():
    p = [0.01, 0.04, 0.03, 0.005]
    # ordenados: 0.005*4=0.02, 0.01*3=0.03, 0.03*2=0.06, 0.04*1=0.04 -> monotônico: 0.06
    np.testing.assert_allclose(stats.holm(p), [0.03, 0.06, 0.06, 0.02])
    assert np.isnan(stats.holm([np.nan, 0.01])[0])
    assert stats.holm([0.9, 0.8]).max() <= 1.0


# --------------------------------------------------------------------------- Wilcoxon


def test_wilcoxon_matches_scipy():
    rng = np.random.default_rng(SEED)
    x, y = rng.normal(10, 1, 25), rng.normal(10.5, 1, 25)
    stat, p = stats.wilcoxon_test(x, y)
    ref = sps.wilcoxon(x, y, alternative="two-sided")
    assert stat == pytest.approx(ref.statistic)
    assert p == pytest.approx(ref.pvalue)


def test_wilcoxon_identical_samples_give_p_one():
    assert stats.wilcoxon_test([1, 2, 3], [1, 2, 3]) == (0.0, 1.0)


def test_min_wilcoxon_p_explains_why_one_machine_with_5_reps_never_rejects():
    assert stats.min_wilcoxon_p(5) == pytest.approx(0.0625)
    assert stats.min_wilcoxon_p(5) > 0.05
    assert stats.min_wilcoxon_p(15) < 0.05 / 5   # 3 máquinas × 5 reps já passa até com Holm


def test_paired_wide_drops_blocks_with_a_failed_install():
    df = _runs({"npm": 1.0, "pnpm": 0.5}, reps=3, machines=("a",))
    df.loc[(df["manager"] == "pnpm") & (df["rep"] == 2), "exit_code"] = 1
    wide = stats.paired_wide(df, ["npm", "pnpm"])
    assert list(wide.columns) == ["npm", "pnpm"]
    assert len(wide) == 2


# --------------------------------------------------------------------------- Todos × npm


def test_compare_to_control_detects_real_speedups_and_not_null_ones():
    effects = {**ALL_EQUAL, "pnpm": 0.5, "bun": 0.4}
    out = stats.compare_to_control(_runs(effects)).set_index("manager")
    assert set(out.index) == set(MANAGERS) - {CONTROL}
    assert out.loc["pnpm", "n_pairs"] == 30
    assert out.loc["pnpm", "reject"] and out.loc["bun", "reject"]
    assert out.loc["pnpm", "speedup"] == pytest.approx(2.0, rel=0.1)
    assert out.loc["pnpm", "cliffs_delta"] < 0   # mais rápido que o npm
    # quem tem o mesmo tempo do npm não deve rejeitar (só ruído)
    assert not out.loc["yarn-classic", "reject"]
    assert (out["p_holm"] >= out["p"]).all()


def test_compare_to_control_matches_scipy_and_holm_per_family():
    df = _runs({**ALL_EQUAL, "pnpm": 0.8})
    out = stats.compare_to_control(df)
    wide = stats.paired_wide(df, [CONTROL, "pnpm"])
    ref = sps.wilcoxon(wide["pnpm"], wide[CONTROL])
    row = out.set_index("manager").loc["pnpm"]
    assert row["p"] == pytest.approx(ref.pvalue)
    np.testing.assert_allclose(out["p_holm"], stats.holm(out["p"]))


def test_compare_to_control_groups_by_project_and_scenario():
    df = pd.concat([_runs(ALL_EQUAL), _runs(ALL_EQUAL).assign(scenario="warm-cache")])
    out = stats.compare_to_control(df)
    assert len(out) == 2 * (len(MANAGERS) - 1)
    assert set(out["scenario"]) == {"cold", "warm-cache"}


# --------------------------------------------------------------------------- Yarn × Yarn


def test_yarn_friedman_matches_scipy_and_posthoc_finds_the_fast_one():
    effects = {"yarn-classic": 1.0, "yarn-berry-nm": 0.95, "yarn-berry-pnp": 0.5}
    df = _runs(effects)
    omnibus, posthoc = stats.yarn_friedman(df)
    wide = stats.paired_wide(df, list(YARN_VARIANTS))
    ref = sps.friedmanchisquare(*(wide[v] for v in YARN_VARIANTS))
    assert omnibus["statistic"].iloc[0] == pytest.approx(ref.statistic)
    assert omnibus["p"].iloc[0] == pytest.approx(ref.pvalue)
    assert omnibus["reject"].iloc[0]
    assert len(posthoc) == 3
    pnp = posthoc[(posthoc["a"] == "yarn-classic") & (posthoc["b"] == "yarn-berry-pnp")].iloc[0]
    assert pnp["reject"] and pnp["ratio"] < 1   # a = Classic é mais lento que o PnP


def test_yarn_friedman_does_not_reject_when_all_equal():
    omnibus, _ = stats.yarn_friedman(_runs({v: 1.0 for v in YARN_VARIANTS}, noise=0.05))
    assert not omnibus["reject"].iloc[0]


# --------------------------------------------------------------------------- dados reais


def test_runs_on_the_committed_data():
    df = load_runs()
    if df.empty:
        df = load_runs(include_synthetic=True)
    vs_npm = stats.compare_to_control(df, n_resamples=200)
    assert not vs_npm.empty and vs_npm["p"].between(0, 1).all()
    omnibus, posthoc = stats.yarn_friedman(df)
    assert not omnibus.empty and len(posthoc) == 3 * len(omnibus)



# --------------------------------------------------------------------------- Yarn × Yarn (T14)


def _yarn_frame():
    """2 máquinas × 3 reps: Classic sempre 2 s, nm 4 s, PnP 1 s (na máquina b, nm < PnP)."""
    rows = []
    for machine in ("a", "b"):
        for rep in (1, 2, 3):
            for manager, wall in (("yarn-classic", 2.0), ("yarn-berry-nm", 4.0),
                                  ("yarn-berry-pnp", 1.0 if machine == "a" else 5.0)):
                rows.append(dict(machine=machine, rep=rep, project="next-app", scenario="ci",
                                 manager=manager, wall_s=wall + rep / 100, disk_mb=1.0,
                                 cache_mb=1.0, exit_code=0, build_ok=True))
    return pd.DataFrame(rows)


def test_yarn_vs_classic_speedup_direction():
    out = stats.yarn_vs_classic(_yarn_frame(), n_resamples=50).set_index("manager")
    assert set(out.index) == {"yarn-berry-nm", "yarn-berry-pnp"}
    assert out.loc["yarn-berry-nm", "speedup"] < 1   # nm mais lento que o Classic
    assert out.loc["yarn-berry-nm", "n_pairs"] == 6


def test_fastest_and_machine_agreement():
    df = _yarn_frame()
    fastest = stats.fastest_by_cell(df, stats.YARN_VARIANTS)
    assert fastest.loc[0, "manager"] == "yarn-classic"   # medianas: Classic 2, PnP 3, nm 4
    agree = stats.machine_agreement(df, stats.YARN_VARIANTS)
    assert agree.loc[0, "n_agree"] == 1 and agree.loc[0, "n_machines"] == 2


# --------------------------------------------------------------------------- Promessas (T18)


def test_compare_claims_classifies_ci_verdicts():
    vs = pd.DataFrame(
        [
            {"project": "next-app", "scenario": "cold", "manager": "pnpm",
             "speedup": 2.0, "speedup_low": 1.5, "speedup_high": 2.5},
            {"project": "next-app", "scenario": "warm-cache", "manager": "pnpm",
             "speedup": 10.0, "speedup_low": 8.0, "speedup_high": 12.0},
            {"project": "express-api", "scenario": "reinstall", "manager": "bun",
             "speedup": 28.0, "speedup_low": 5.0, "speedup_high": 35.0},
        ]
    )
    out = stats.compare_claims(vs).set_index(["manager", "scenario"])
    assert out.loc[("pnpm", "cold"), "status"] == "Abaixo do anunciado"
    assert out.loc[("pnpm", "warm-cache"), "status"] == "Supera o anunciado"
    assert out.loc[("bun", "reinstall"), "status"] == "Confirma (no IC 95%)"
