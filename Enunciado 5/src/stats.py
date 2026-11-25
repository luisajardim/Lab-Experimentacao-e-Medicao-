"""Análise estatística do Lab05: descritiva, testes e tamanho do efeito.

- **Descritiva por célula** (projeto × cenário × gerenciador): n, mediana, quartis, IQR, p90 e
  taxa de instalações válidas.
- **Todos × npm:** Wilcoxon pareado bicaudal de cada gerenciador contra o controle, com correção
  de Holm dentro de cada família (as 5 comparações de um projeto × cenário).
- **Yarn × Yarn:** Friedman entre as 3 variantes do Yarn + post-hoc de Wilcoxon pareado com Holm.
  Para os gráficos: speedup do Berry em relação ao Classic e o mais rápido por célula e máquina
  (T14, #111).
- **Tamanho do efeito:** Cliff's δ (com a magnitude de Romano et al., 2006) e speedup = mediana do
  controle / mediana do tratamento (> 1: mais rápido que o npm), com IC 95% por bootstrap pareado.

Pareamento: uma instalação de cada gerenciador com a mesma **máquina, projeto, cenário e
repetição** forma um bloco. Só entram instalações válidas (`exit_code == 0` e `build_ok`); um
bloco em que algum lado falhou sai do teste (a taxa de falhas é resultado à parte, em `describe`).

Validado contra `scipy.stats.wilcoxon` e `scipy.stats.friedmanchisquare` em `tests/test_stats.py`.

Issues: #103 (T08), #111 (T14).
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd
from scipy import stats

from config import ALPHA, CONTROL, MANAGERS, SEED, YARN_VARIANTS

BLOCK = ("machine", "rep")                 # dentro de um projeto × cenário
GROUP = ("project", "scenario")            # uma família de comparações
CELL = (*GROUP, "manager")
BOOTSTRAP_RESAMPLES = 2_000
CONFIDENCE = 0.95

# Limiares de |δ| de Romano et al. (2006), os mais usados em engenharia de software.
CLIFF_THRESHOLDS = ((0.147, "desprezível"), (0.33, "pequeno"), (0.474, "médio"))
CLIFF_LARGE = "grande"


# --------------------------------------------------------------------------- preparação


def add_derived(df: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta `footprint_mb` = `disk_mb + cache_mb` (pegada total em disco)."""
    return df.assign(footprint_mb=df["disk_mb"] + df["cache_mb"])


def valid_runs(df: pd.DataFrame) -> pd.DataFrame:
    """Só as instalações válidas: terminaram com código 0 e o `build` passou."""
    return df[(df["exit_code"] == 0) & df["build_ok"].astype(bool)]


# --------------------------------------------------------------------------- descritiva


def describe(df: pd.DataFrame, metric: str = "wall_s", by: Sequence[str] = CELL) -> pd.DataFrame:
    """Descritiva por célula sobre as instalações válidas + taxa de válidas sobre todas."""
    df = add_derived(df)
    by = list(by)
    valid = valid_runs(df)
    grouped = valid.groupby(by, observed=True)[metric]
    out = pd.DataFrame(
        {
            "n": grouped.size(),
            "median": grouped.median(),
            "q1": grouped.quantile(0.25),
            "q3": grouped.quantile(0.75),
            "p90": grouped.quantile(0.90),
            "mean": grouped.mean(),
        }
    )
    out["iqr"] = out["q3"] - out["q1"]
    ok = (df["exit_code"] == 0) & df["build_ok"].astype(bool)
    out["valid_rate"] = ok.groupby([df[c] for c in by], observed=True).mean()
    out["n_total"] = df.groupby(by, observed=True).size()
    out = out.reset_index()
    out["n"] = out["n"].fillna(0).astype(int)
    return out


# --------------------------------------------------------------------------- tamanho do efeito


def cliffs_delta(x, y) -> float:
    """Cliff's δ = P(X > Y) − P(X < Y), entre −1 e 1 (amostras independentes)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size == 0 or y.size == 0:
        return float("nan")
    diff = np.sign(x[:, None] - y[None, :])
    return float(diff.mean())


def cliff_magnitude(delta: float) -> str:
    """Rótulo da magnitude de |δ| (Romano et al., 2006)."""
    if np.isnan(delta):
        return "—"
    size = abs(delta)
    for limit, label in CLIFF_THRESHOLDS:
        if size < limit:
            return label
    return CLIFF_LARGE


def speedup(control, treatment) -> float:
    """Razão das medianas: mediana(controle) / mediana(tratamento). > 1 = tratamento mais rápido."""
    treat_median = float(np.median(treatment))
    if treat_median == 0:
        return float("inf")
    return float(np.median(control)) / treat_median


def speedup_ci(control, treatment, n_resamples: int = BOOTSTRAP_RESAMPLES, seed: int = SEED,
               confidence: float = CONFIDENCE) -> tuple[float, float]:
    """IC do speedup por bootstrap **pareado** (reamostra os blocos), percentil.

    Usa percentil, e não BCa, porque com poucas repetições e tempos empatados o BCa fica instável.
    """
    control = np.asarray(control, dtype=float)
    treatment = np.asarray(treatment, dtype=float)
    if control.size < 2:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, control.size, size=(n_resamples, control.size))
    num = np.median(control[idx], axis=1)
    den = np.median(treatment[idx], axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratios = num / den
    tail = (1 - confidence) / 2
    low, high = np.quantile(ratios, [tail, 1 - tail])
    return float(low), float(high)


# --------------------------------------------------------------------------- correção múltipla


def holm(pvalues) -> np.ndarray:
    """p-valores ajustados por Holm (step-down), na ordem original. NaN continua NaN."""
    p = np.asarray(pvalues, dtype=float)
    adjusted = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    m = int(ok.sum())
    if m == 0:
        return adjusted
    order = np.argsort(p[ok])
    ranked = p[ok][order] * (m - np.arange(m))
    ranked = np.minimum(np.maximum.accumulate(ranked), 1.0)
    values = np.empty(m)
    values[order] = ranked
    adjusted[ok] = values
    return adjusted


# --------------------------------------------------------------------------- pareamento


def paired_wide(df: pd.DataFrame, managers: Sequence[str], metric: str = "wall_s") -> pd.DataFrame:
    """Tabela larga de um projeto × cenário: uma linha por bloco (máquina, rep), uma coluna por
    gerenciador; só blocos em que **todos** os `managers` têm instalação válida."""
    df = add_derived(valid_runs(df))
    sub = df[df["manager"].isin(managers)]
    wide = sub.pivot_table(index=list(BLOCK), columns="manager", values=metric,
                           aggfunc="first", observed=True)
    missing = [m for m in managers if m not in wide.columns]
    for m in missing:
        wide[m] = np.nan
    return wide[list(managers)].dropna()


def wilcoxon_test(x, y) -> tuple[float, float]:
    """Wilcoxon pareado bicaudal; devolve (estatística, p). Sem diferença nenhuma: p = 1."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size == 0:
        return float("nan"), float("nan")
    if np.all(x - y == 0):
        return 0.0, 1.0
    res = stats.wilcoxon(x, y, alternative="two-sided")
    return float(res.statistic), float(res.pvalue)


def min_wilcoxon_p(n_pairs: int) -> float:
    """Menor p bicaudal exato possível do Wilcoxon com `n_pairs` pares: 2 / 2ⁿ."""
    return min(1.0, 2.0 / 2**n_pairs)


# --------------------------------------------------------------------------- Todos × npm


def compare_to_control(df: pd.DataFrame, metric: str = "wall_s", control: str = CONTROL,
                       group: Sequence[str] = GROUP, alpha: float = ALPHA,
                       n_resamples: int = BOOTSTRAP_RESAMPLES, seed: int = SEED) -> pd.DataFrame:
    """Cada gerenciador × controle, em cada grupo (projeto × cenário por padrão).

    Holm é aplicado dentro de cada grupo (família = as comparações contra o controle).
    Colunas: grupo, `manager`, `n_pairs`, medianas, `speedup` + IC, `cliffs_delta` (tratamento
    vs. controle: negativo = tratamento mais rápido), magnitude, estatística, `p`, `p_holm`,
    `reject`.
    """
    group = list(group)
    treatments = [m for m in MANAGERS if m != control]
    rows = []
    for key, sub in df.groupby(group, observed=True, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        family = []
        for manager in treatments:
            wide = paired_wide(sub, [control, manager], metric)
            c, t = wide[control].to_numpy(), wide[manager].to_numpy()
            stat, p = wilcoxon_test(t, c)
            low, high = speedup_ci(c, t, n_resamples=n_resamples, seed=seed)
            delta = cliffs_delta(t, c)
            family.append(
                {
                    **dict(zip(group, key, strict=True)),
                    "manager": manager,
                    "n_pairs": int(len(wide)),
                    "median_control": float(np.median(c)) if len(c) else np.nan,
                    "median_manager": float(np.median(t)) if len(t) else np.nan,
                    "speedup": speedup(c, t) if len(c) else np.nan,
                    "speedup_low": low,
                    "speedup_high": high,
                    "cliffs_delta": delta,
                    "magnitude": cliff_magnitude(delta),
                    "statistic": stat,
                    "p": p,
                }
            )
        p_adj = holm([r["p"] for r in family])
        for row, adj in zip(family, p_adj, strict=True):
            row["p_holm"] = float(adj)
            row["reject"] = bool(adj < alpha) if not np.isnan(adj) else False
        rows.extend(family)
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- Yarn × Yarn


def yarn_friedman(df: pd.DataFrame, metric: str = "wall_s", variants: Sequence[str] = YARN_VARIANTS,
                  group: Sequence[str] = GROUP, alpha: float = ALPHA) -> tuple[pd.DataFrame,
                                                                                 pd.DataFrame]:
    """Friedman entre as variantes do Yarn + post-hoc Wilcoxon com Holm, por grupo.

    Devolve `(friedman, posthoc)`. No post-hoc, `cliffs_delta` é de `a` contra `b`
    (negativo = `a` mais rápido) e o Holm vale dentro de cada grupo (3 pares).
    """
    group = list(group)
    variants = list(variants)
    pairs = [(a, b) for i, a in enumerate(variants) for b in variants[i + 1:]]
    omnibus, posthoc = [], []
    for key, sub in df.groupby(group, observed=True, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        labels = dict(zip(group, key, strict=True))
        wide = paired_wide(sub, variants, metric)
        n_blocks = int(len(wide))
        if n_blocks >= 2:
            try:
                res = stats.friedmanchisquare(*(wide[v].to_numpy() for v in variants))
                stat, p = float(res.statistic), float(res.pvalue)
            except ValueError:
                stat, p = float("nan"), float("nan")
        else:
            stat, p = float("nan"), float("nan")
        omnibus.append(
            {
                **labels,
                "n_blocks": n_blocks,
                **{f"median_{v}": float(wide[v].median()) if n_blocks else np.nan
                   for v in variants},
                "statistic": stat,
                "p": p,
                "reject": bool(p < alpha) if not np.isnan(p) else False,
            }
        )
        family = []
        for a, b in pairs:
            w_stat, w_p = wilcoxon_test(wide[a].to_numpy(), wide[b].to_numpy())
            delta = cliffs_delta(wide[a].to_numpy(), wide[b].to_numpy())
            family.append(
                {
                    **labels,
                    "a": a,
                    "b": b,
                    "n_blocks": n_blocks,
                    "median_a": float(wide[a].median()) if n_blocks else np.nan,
                    "median_b": float(wide[b].median()) if n_blocks else np.nan,
                    "ratio": speedup(wide[b], wide[a]) if n_blocks else np.nan,
                    "cliffs_delta": delta,
                    "magnitude": cliff_magnitude(delta),
                    "statistic": w_stat,
                    "p": w_p,
                }
            )
        for row, adj in zip(family, holm([r["p"] for r in family]), strict=True):
            row["p_holm"] = float(adj)
            row["reject"] = bool(adj < alpha) if not np.isnan(adj) else False
        posthoc.extend(family)
    return pd.DataFrame(omnibus), pd.DataFrame(posthoc)


YARN_BASE = "yarn-classic"   # referência da aba Yarn × Yarn: a versão mais antiga do mesmo software


def yarn_vs_classic(df: pd.DataFrame, metric: str = "wall_s", base: str = YARN_BASE,
                    variants: Sequence[str] = YARN_VARIANTS, group: Sequence[str] = GROUP,
                    n_resamples: int = BOOTSTRAP_RESAMPLES, seed: int = SEED) -> pd.DataFrame:
    """Speedup de cada variante do Berry em relação ao Classic, por grupo, com IC 95% pareado.

    Mesmas colunas que `compare_to_control` usa no gráfico (`speedup`, `speedup_low`,
    `speedup_high`); a inferência fica com `yarn_friedman`, este é só o tamanho do efeito.
    """
    group = list(group)
    rows = []
    for key, sub in df.groupby(group, observed=True, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        for manager in (v for v in variants if v != base):
            wide = paired_wide(sub, [base, manager], metric)
            c, t = wide[base].to_numpy(), wide[manager].to_numpy()
            low, high = speedup_ci(c, t, n_resamples=n_resamples, seed=seed)
            rows.append({
                **dict(zip(group, key, strict=True)),
                "manager": manager,
                "n_pairs": int(len(wide)),
                "median_control": float(np.median(c)) if len(c) else np.nan,
                "median_manager": float(np.median(t)) if len(t) else np.nan,
                "speedup": speedup(c, t) if len(c) else np.nan,
                "speedup_low": low,
                "speedup_high": high,
            })
    return pd.DataFrame(rows)


def fastest_by_cell(df: pd.DataFrame, managers: Sequence[str], metric: str = "wall_s",
                    by: Sequence[str] = GROUP) -> pd.DataFrame:
    """O gerenciador de menor mediana (instalações válidas) em cada grupo de `by`."""
    sub = add_derived(valid_runs(df))
    sub = sub[sub["manager"].isin(managers)]
    if sub.empty:
        return pd.DataFrame(columns=[*by, "manager", "median"])
    med = sub.groupby([*by, "manager"], observed=True)[metric].median().rename("median")
    best = med.reset_index().sort_values("median", kind="stable")
    return best.drop_duplicates(list(by)).sort_values(list(by)).reset_index(drop=True)


def machine_agreement(df: pd.DataFrame, managers: Sequence[str],
                      metric: str = "wall_s") -> pd.DataFrame:
    """Para cada projeto × cenário, o mais rápido no geral e em quantas máquinas ele também é."""
    overall = fastest_by_cell(df, managers, metric)
    per_machine = fastest_by_cell(df, managers, metric, by=("machine", *GROUP))
    merged = per_machine.merge(overall[[*GROUP, "manager"]], on=list(GROUP),
                               suffixes=("_machine", ""))
    agree = (merged["manager_machine"] == merged["manager"]).groupby(
        [merged[c] for c in GROUP]).agg(["sum", "size"])
    agree.columns = ["n_agree", "n_machines"]
    return overall.merge(agree.reset_index(), on=list(GROUP), how="left")
