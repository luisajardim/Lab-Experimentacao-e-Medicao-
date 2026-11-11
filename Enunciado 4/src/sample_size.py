"""Extra: tamanho da amostra × poder e erro tipo I (seção 6 do enunciado, "Para discutir").

Simula as situações S-real e S-outlier variando o número de classes n, para
três efeitos: ρ = 0 (erro tipo I), um efeito moderado (ρ latente = 0,3) e o efeito
observado na amostra real (ρ latente calibrado para que o ρₛ populacional do
gerador seja igual ao ρₛ da amostra de 30 classes). Responde:
- qual o poder de cada teste com o n coletado (30) para o efeito observado;
- quantas classes seriam necessárias para 80% de poder;
- se as violações de pressupostos pesam mais com amostras pequenas ou grandes.

É opcional e mais lenta (~2 min), por isso só roda quando pedida:
`uv run lab04 --sample-size` ou `uv run python -m sample_size [--force]`.
Os resultados ficam em `data/sim/sample_size.csv` e são versionados, então o
dashboard os mostra sem precisar rodar a simulação.

Issue: #91 (T14).
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import simulate
from config import ALPHAS, COLOR_PEARSON, COLOR_SPEARMAN, DATA_SIM, DEFAULT_ALPHA, REPS
from data import SAMPLE_CSV
from generate import generate
from stat_tests import pearson, spearman

RESULTS_FILE = "sample_size.csv"
META_FILE = "sample_size_meta.json"
SITUATIONS = ("S-real", "S-outlier")
N_GRID = (10, 20, 30, 50, 80, 120, 200)
N_REAL = 30
MODERATE_RHO = 0.3
TARGET_POWER = 0.8
EFFECT_LABELS = {"zero": "sem efeito (ρ = 0)", "moderado": "efeito moderado", "observado": "efeito observado"}
TESTS = {"pearson": ("Pearson", COLOR_PEARSON), "spearman": ("Spearman", COLOR_SPEARMAN)}


def observed_rho_s(sample_csv: Path = SAMPLE_CSV) -> float:
    """ρₛ da amostra real de 30 classes."""
    df = pd.read_csv(sample_csv)
    return float(spearman(df["loc"].to_numpy(float), df["defects"].to_numpy(float)).coef)


def calibrate_latent_rho(situation: str, target_rho_s: float, population: pd.DataFrame) -> float:
    """ρ latente cujo ρₛ populacional (em `population.csv`) é `target_rho_s`, por interpolação."""
    rows = population[population["situation"] == situation].sort_values("rho")
    if not rows["rho_s_pop"].min() <= target_rho_s <= rows["rho_s_pop"].max():
        raise ValueError(f"ρₛ = {target_rho_s:.3f} fora da grade de {situation}")
    return round(float(np.interp(target_rho_s, rows["rho_s_pop"], rows["rho"])), 3)


def effects_for(situation: str, target_rho_s: float, population: pd.DataFrame) -> dict[str, float]:
    return {
        "zero": 0.0,
        "moderado": MODERATE_RHO,
        "observado": calibrate_latent_rho(situation, target_rho_s, population),
    }


def simulate_n_cell(situation: str, rho: float, n: int, reps: int) -> dict[str, np.ndarray]:
    """p-valores dos dois testes em `reps` conjuntos de `n` classes."""
    rng = simulate.cell_rng(f"{situation}|n={n}", rho, purpose=2)
    x, y = generate(situation, rho, n=n, reps=reps, rng=rng)
    return {"pearson": pearson(x, y).p, "spearman": spearman(x, y).p}


def config_snapshot(reps: int, target_rho_s: float) -> dict:
    code = {
        name: simulate.file_sha256(simulate.SRC_DIR / name)
        for name in (*simulate.CODE_FILES, "sample_size.py")
    }
    return {
        "base": simulate.config_snapshot(simulate.REPS),
        "reps": reps,
        "situations": list(SITUATIONS),
        "n_grid": list(N_GRID),
        "moderate_rho": MODERATE_RHO,
        "observed_rho_s": round(target_rho_s, 6),
        "code_sha256": code,
    }


def run(reps: int = REPS, out_dir: Path = DATA_SIM, force: bool = False, verbose: bool = True) -> pd.DataFrame:
    """Roda (ou reaproveita do cache) a simulação por n e grava `sample_size.csv`."""
    population = simulate.load_population(out_dir)
    target = observed_rho_s()
    snapshot = config_snapshot(reps, target)
    key = simulate.cache_key(snapshot)
    meta_path, results_path = out_dir / META_FILE, out_dir / RESULTS_FILE
    cached = results_path.exists() and meta_path.exists()
    if not force and cached and json.loads(meta_path.read_text()).get("cache_key") == key:
        if verbose:
            print("[sample_size] Resultados já batem com a configuração (cache).")
        return pd.read_csv(results_path)

    start = time.perf_counter()
    rows = []
    for situation in SITUATIONS:
        for label, rho in effects_for(situation, target, population).items():
            for n in N_GRID:
                pvals = simulate_n_cell(situation, rho, n, reps)
                for test, p in pvals.items():
                    for alpha in ALPHAS:
                        rate = float(np.mean(p < alpha))
                        rows.append({
                            "situation": situation, "effect": label, "rho": rho, "n": n,
                            "alpha": alpha, "test": test, "reject_rate": rate,
                            "mc_se": float(np.sqrt(rate * (1 - rate) / reps)),
                            "n_nan": int(np.isnan(p).sum()),
                        })
        if verbose:
            print(f"[sample_size] {situation}: 3 efeitos × {len(N_GRID)} valores de n × {reps} réplicas")
    results = pd.DataFrame(rows)
    elapsed = time.perf_counter() - start
    out_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(results_path, index=False)
    meta = {"cache_key": key, "config": snapshot, "elapsed_seconds": round(elapsed, 1)}
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    if verbose:
        print(f"[sample_size] Concluído em {elapsed:.1f} s → {results_path}")
    return results


def load(out_dir: Path = DATA_SIM) -> pd.DataFrame | None:
    path = out_dir / RESULTS_FILE
    return pd.read_csv(path) if path.exists() else None


def n_for_power(curve: pd.DataFrame, target: float = TARGET_POWER) -> float:
    """Menor n (interpolado em log n) com poder ≥ `target`; NaN se não alcança na grade."""
    curve = curve.sort_values("n")
    n, power = curve["n"].to_numpy(float), curve["reject_rate"].to_numpy()
    above = np.flatnonzero(power >= target)
    if above.size == 0:
        return float("nan")
    i = above[0]
    if i == 0:
        return float(n[0])
    # interpolação linear do poder em função de log(n)
    frac = (target - power[i - 1]) / (power[i] - power[i - 1])
    return float(np.exp(np.log(n[i - 1]) + frac * (np.log(n[i]) - np.log(n[i - 1]))))


def n80_table(results: pd.DataFrame, alpha: float = DEFAULT_ALPHA) -> pd.DataFrame:
    """Poder com n = 30 e n necessário para 80% de poder, por situação × efeito × teste."""
    rows = []
    sub = results[(results["alpha"] == alpha) & (results["effect"] != "zero")]
    for (situation, effect, test), curve in sub.groupby(["situation", "effect", "test"], sort=False):
        rows.append({
            "situation": situation, "effect": effect, "rho": curve["rho"].iloc[0], "test": test,
            "power_n30": float(curve.loc[curve["n"] == N_REAL, "reject_rate"].iloc[0]),
            "n80": n_for_power(curve),
        })
    return pd.DataFrame(rows)


def _dec(v: float, digits: int = 2) -> str:
    return f"{v:.{digits}f}".replace(".", ",")


def _pct(v: float) -> str:
    return f"{v:.0%}".replace(".", ",")


def _n_text(v: float) -> str:
    return f"mais de {max(N_GRID)}" if np.isnan(v) else f"cerca de {int(np.ceil(v))}"


def summary_text(results: pd.DataFrame, alpha: float = DEFAULT_ALPHA) -> str:
    """Texto curto (até 4 frases), montado a partir dos números."""
    table = n80_table(results, alpha).set_index(["situation", "effect", "test"]).sort_index()
    obs = table.loc["S-real", "observado"]
    mod = table.loc["S-real", "moderado"]
    zero = results[(results["alpha"] == alpha) & (results["effect"] == "zero")
                   & (results["situation"] == "S-outlier") & (results["test"] == "pearson")]
    t1_small = zero.loc[zero["n"] == min(N_GRID), "reject_rate"].item()
    t1_large = zero.loc[zero["n"] == max(N_GRID), "reject_rate"].item()
    return (
        f"Com as {N_REAL} classes coletadas e o efeito observado (ρₛ ≈ {_dec(observed_rho_s())}), "
        f"na S-real o Pearson tem poder de {_pct(obs.loc['pearson', 'power_n30'])} e o Spearman de "
        f"{_pct(obs.loc['spearman', 'power_n30'])}; para 80% de poder bastariam "
        f"{_n_text(obs.loc['pearson', 'n80'])} classes com o Pearson e {_n_text(obs.loc['spearman', 'n80'])} "
        f"com o Spearman, o que é viável de coletar. Com um efeito moderado (ρ latente = 0,3), seriam "
        f"necessárias {_n_text(mod.loc['pearson', 'n80'])} (Pearson) e {_n_text(mod.loc['spearman', 'n80'])} "
        f"(Spearman) classes. Na S-outlier, o erro tipo I do Pearson vai de {_pct(t1_small)} com n = "
        f"{min(N_GRID)} a {_pct(t1_large)} com n = {max(N_GRID)}: aumentar a amostra não corrige a "
        f"violação, porque mais classes trazem mais chances de uma classe extrema."
    )


def fig_sample_size(results: pd.DataFrame, alpha: float = DEFAULT_ALPHA):
    """Poder × n (linha em 80%) e erro tipo I × n (linha em α), por situação."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    sub = results[results["alpha"] == alpha]
    fig = make_subplots(
        rows=2, cols=len(SITUATIONS), shared_xaxes=True, vertical_spacing=0.12, horizontal_spacing=0.08,
        subplot_titles=[f"{s}: poder" for s in SITUATIONS] + [f"{s}: erro tipo I (ρ = 0)" for s in SITUATIONS],
    )
    dash = {"observado": "solid", "moderado": "dash", "zero": "solid"}
    for col, situation in enumerate(SITUATIONS, start=1):
        for test, (name, color) in TESTS.items():
            for effect in ("observado", "moderado", "zero"):
                curve = sub[(sub["situation"] == situation) & (sub["test"] == test)
                            & (sub["effect"] == effect)].sort_values("n")
                rho = curve["rho"].iloc[0]
                label = f"{name} — {EFFECT_LABELS[effect]}" + ("" if effect == "zero" else f" (ρ latente = {rho:.2f})")
                fig.add_trace(
                    go.Scatter(
                        x=curve["n"], y=curve["reject_rate"], mode="lines+markers",
                        line=dict(color=color, dash=dash[effect], width=2),
                        name=label.replace(".", ","), legendgroup=f"{test}-{effect}",
                        showlegend=col == 1,
                        hovertemplate=f"{name}<br>n = %{{x}}<br>Rejeições: %{{y:.1%}}<extra></extra>",
                    ),
                    row=2 if effect == "zero" else 1, col=col,
                )
        fig.add_hline(y=TARGET_POWER, line=dict(color="#2C3E50", dash="dot"), row=1, col=col,
                      annotation_text="80% de poder", annotation_position="bottom right")
        fig.add_hline(y=alpha, line=dict(color="#2C3E50", dash="dot"), row=2, col=col,
                      annotation_text=f"α = {alpha:.0%}", annotation_position="top right")
    fig.update_xaxes(type="log", tickvals=list(N_GRID), title_text="Tamanho da amostra n (classes, escala log)", row=2)
    fig.update_xaxes(type="log", tickvals=list(N_GRID), row=1)
    fig.update_yaxes(title_text="Proporção de rejeições de H₀", tickformat=".0%", range=[0, 1.02], row=1)
    fig.update_yaxes(title_text="Proporção de rejeições de H₀", tickformat=".0%", rangemode="tozero", row=2)
    fig.update_layout(
        title=dict(text=f"Extra — Poder e erro tipo I × tamanho da amostra (α = {alpha:.2f})".replace(".", ","),
                   x=0.0, xanchor="left"),
        height=700, template="plotly_white", separators=",.",
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="left", x=0.0),
        margin=dict(t=80, b=150, l=70, r=30),
    )
    return fig


def render_section(alpha: float = DEFAULT_ALPHA) -> None:
    """Bloco do dashboard; não mostra nada se a simulação extra ainda não foi gerada."""
    import streamlit as st

    results = load()
    if results is None:
        return
    st.header("Para discutir: tamanho da amostra")
    st.plotly_chart(fig_sample_size(results, alpha), width="stretch")
    st.markdown(summary_text(results, alpha))
    with st.expander("Poder com n = 30 e n necessário para 80% de poder"):
        table = n80_table(results, alpha)
        table["test"] = table["test"].map(lambda t: TESTS[t][0])
        table["effect"] = table["effect"].map(EFFECT_LABELS)
        table = table.rename(columns={
            "situation": "Situação", "effect": "Efeito", "rho": "ρ latente", "test": "Teste",
            "power_n30": "Poder com n = 30", "n80": "n para 80% de poder",
        })
        st.dataframe(table.round({"ρ latente": 2, "Poder com n = 30": 3, "n para 80% de poder": 0}),
                     width="stretch", hide_index=True)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Extra do Lab04: poder e erro tipo I × tamanho da amostra.")
    parser.add_argument("--force", action="store_true", help="re-simula mesmo com cache válido")
    parser.add_argument("--reps", type=int, default=REPS, help=f"réplicas por célula ({REPS})")
    args = parser.parse_args([] if argv is None else argv)
    run(reps=args.reps, force=args.force)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
