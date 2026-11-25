"""Adoção (downloads do registry) cruzada com o desempenho medido no experimento (T16, #113).

Lê os CSVs da T15 (`data/npm_downloads/`, ver [docs/fonte_downloads.md]) e produz as três coisas
que a aba "Adoção × desempenho" precisa:

1. **Séries temporais** de downloads, em valor absoluto e em participação.
2. **Crescimento no último ano**, por pacote.
3. **Adoção × speedup** contra o npm, um ponto por gerenciador.

Duas decisões de método moram aqui, e as duas existem por causa das ameaças de construto da §4 de
`docs/fonte_downloads.md`:

- **Só a era da ferramenta.** Três dos cinco nomes de pacote já existiam no registry ocupados por
  outro software (24,1 % do histórico de `bun` é de outro pacote). Tudo aqui filtra
  `tool_era == True` por padrão.
- **O npm não entra na comparação de níveis.** Ele vem com o Node.js e por isso quase não é
  baixado: comparar o volume dele com o dos outros não mede adoção, mede quem precisa do registry
  para se instalar. No cruzamento com desempenho o npm aparece como **referência** (speedup = 1),
  nunca como um ponto no eixo de downloads.

O speedup agregado por gerenciador é a **média geométrica** dos speedups das células (projeto ×
cenário). Média geométrica porque speedup é razão: a média aritmética de 0,5× e 2,0× daria 1,25×,
quando o resultado correto é 1,0×. A dispersão entre células é reportada como **amplitude**
(mínimo e máximo observados), que **não é** intervalo de confiança — o IC por bootstrap existe por
célula, em `stats.compare_to_control`, e não se combina por média geométrica.

Issues: #113 (T16); dados da #112 (T15).
"""

from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd

import stats
from config import CONTROL, MANAGERS, PALETTE
from npm_downloads import DAILY_CSV, META_CSV, PACKAGES, WEEKLY_CSV

# Pacote que representa cada tratamento, derivado de `PACKAGES` para não haver duas verdades.
# Os dois linkers do Berry apontam para o mesmo pacote: o linker é configuração, não pacote.
PACKAGE_OF_MANAGER: dict[str, str] = {
    manager: package
    for package, info in PACKAGES.items()
    for manager in info["treatments"]
}

# Cor de cada pacote: a do primeiro tratamento que ele representa, para a aba ficar coerente
# com o resto do dashboard (`config.PALETTE`).
PACKAGE_PALETTE: dict[str, str] = {
    package: PALETTE[info["treatments"][0]] for package, info in PACKAGES.items()
}

PACKAGE_LABELS: dict[str, str] = {p: info["label"] for p, info in PACKAGES.items()}

WINDOW_DAYS = 7         # "última semana", como o próprio npm reporta
YEAR_DAYS = 365


# --------------------------------------------------------------------------- leitura


def available() -> bool:
    """Há séries coletadas para a aba usar?"""
    return DAILY_CSV.exists() and WEEKLY_CSV.exists()


def load_daily(path=DAILY_CSV, tool_era_only: bool = True) -> pd.DataFrame:
    """Série diária: `package`, `day` (datetime), `downloads`, `tool_era`."""
    if not path.exists():
        return pd.DataFrame(columns=["package", "day", "downloads", "tool_era"])
    df = pd.read_csv(path, parse_dates=["day"])
    df["tool_era"] = df["tool_era"].astype(str).str.lower().eq("true")
    return df[df["tool_era"]].reset_index(drop=True) if tool_era_only else df


def load_weekly(path=WEEKLY_CSV, tool_era_only: bool = True,
                complete_only: bool = True) -> pd.DataFrame:
    """Série semanal. `complete_only` tira as semanas de borda, que somam menos de 7 dias.

    Sem esse corte a última semana sempre aparece como queda num gráfico de linha — um artefato
    do recorte da coleta, não um movimento do dado.
    """
    if not path.exists():
        return pd.DataFrame(columns=["package", "week_start", "downloads", "days",
                                     "complete_week", "tool_era"])
    df = pd.read_csv(path, parse_dates=["week_start"])
    for col in ("complete_week", "tool_era"):
        df[col] = df[col].astype(str).str.lower().eq("true")
    if tool_era_only:
        df = df[df["tool_era"]]
    if complete_only:
        df = df[df["complete_week"]]
    return df.reset_index(drop=True)


def load_meta(path=META_CSV) -> pd.DataFrame:
    """Metadados por pacote, incluindo `fetched_at` (a data da coleta)."""
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def fetched_at(path=META_CSV) -> str:
    """Data da coleta das séries, para creditar na figura. Vazio se não houver metadados."""
    meta = load_meta(path)
    return str(meta["fetched_at"].iloc[0]) if not meta.empty else ""


# --------------------------------------------------------------------------- séries e totais


def add_share(weekly: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta `share`: a fatia de cada pacote no total **daquela semana**.

    A fatia só faz sentido entre os cinco pacotes coletados e, por causa do npm vir com o Node,
    não é participação de mercado. A figura diz isso no subtítulo.
    """
    if weekly.empty:
        return weekly.assign(share=pd.Series(dtype=float))
    total = weekly.groupby("week_start")["downloads"].transform("sum")
    return weekly.assign(share=(weekly["downloads"] / total.replace(0, np.nan)).fillna(0.0))


def window_total(daily: pd.DataFrame, days: int = WINDOW_DAYS,
                 until: pd.Timestamp | None = None) -> pd.Series:
    """Downloads por pacote nos últimos `days` dias que terminam em `until` (padrão: o último dia)."""
    if daily.empty:
        return pd.Series(dtype="int64")
    end = pd.Timestamp(until) if until is not None else daily["day"].max()
    start = end - pd.Timedelta(int(days) - 1, unit="D")
    janela = daily[(daily["day"] >= start) & (daily["day"] <= end)]
    return janela.groupby("package")["downloads"].sum()


def adoption_table(daily: pd.DataFrame, until: pd.Timestamp | None = None,
                   window_days: int = WINDOW_DAYS, year_days: int = YEAR_DAYS) -> pd.DataFrame:
    """Uma linha por pacote: volume recente, fatia e crescimento no último ano.

    Colunas: `package`, `label`, `downloads_window`, `share_window`, `downloads_year`,
    `downloads_prev_year`, `growth` (razão ano atual / ano anterior) e `growth_pct`.
    """
    if daily.empty:
        return pd.DataFrame(columns=["package", "label", "downloads_window", "share_window",
                                     "downloads_year", "downloads_prev_year", "growth",
                                     "growth_pct"])
    end = pd.Timestamp(until) if until is not None else daily["day"].max()
    janela = window_total(daily, window_days, end)
    ano = window_total(daily, year_days, end)
    anterior = window_total(daily, year_days,
                            end - pd.Timedelta(int(year_days), unit="D"))
    total_janela = float(janela.sum())

    rows = []
    for package in PACKAGES:
        atual, passado = int(ano.get(package, 0)), int(anterior.get(package, 0))
        semana = int(janela.get(package, 0))
        crescimento = atual / passado if passado else np.nan
        rows.append({
            "package": package,
            "label": PACKAGE_LABELS[package],
            "downloads_window": semana,
            "share_window": semana / total_janela if total_janela else np.nan,
            "downloads_year": atual,
            "downloads_prev_year": passado,
            "growth": crescimento,
            "growth_pct": (crescimento - 1) * 100 if np.isfinite(crescimento) else np.nan,
        })
    return pd.DataFrame(rows).sort_values("downloads_year", ascending=False, ignore_index=True)


# --------------------------------------------------------------------------- desempenho agregado


def overall_speedup(runs: pd.DataFrame, metric: str = "wall_s",
                    control: str = CONTROL) -> pd.DataFrame:
    """Speedup de cada gerenciador contra o controle, agregado pelas células (projeto × cenário).

    `speedup_geo` é a média geométrica dos speedups das células; `speedup_min` e `speedup_max` são
    a **amplitude observada** entre elas, não um intervalo de confiança (ver o docstring do
    módulo). `n_cells` é quantas células entraram.
    """
    vazio = pd.DataFrame(columns=["manager", "speedup_geo", "speedup_min", "speedup_max",
                                  "n_cells"])
    if runs.empty:
        return vazio
    cells = stats.compare_to_control(runs, metric=metric, control=control)
    if cells.empty:
        return vazio
    rows = []
    for manager, sub in cells.groupby("manager", observed=True):
        valores = sub["speedup"].replace([np.inf, -np.inf], np.nan).dropna()
        valores = valores[valores > 0]
        if valores.empty:
            continue
        rows.append({
            "manager": manager,
            "speedup_geo": float(np.exp(np.log(valores).mean())),
            "speedup_min": float(valores.min()),
            "speedup_max": float(valores.max()),
            "n_cells": int(len(valores)),
        })
    out = pd.DataFrame(rows)
    if out.empty:
        return vazio
    order = {m: i for i, m in enumerate(MANAGERS)}
    return out.sort_values("manager", key=lambda s: s.map(order), ignore_index=True)


def adoption_vs_performance(runs: pd.DataFrame, daily: pd.DataFrame, metric: str = "wall_s",
                            until: pd.Timestamp | None = None, year_days: int = YEAR_DAYS,
                            control: str = CONTROL) -> pd.DataFrame:
    """Um ponto por gerenciador: adoção no último ano × speedup contra o npm.

    O controle fica **fora**: o speedup dele é 1 por definição e o volume de downloads dele não é
    comparável (vem com o Node.js). Na figura ele é a linha de referência.

    Colunas: `manager`, `label`, `package`, `package_label`, `downloads_year`, `speedup_geo`,
    `speedup_min`, `speedup_max`, `n_cells`, `shared_package`.
    """
    desempenho = overall_speedup(runs, metric=metric, control=control)
    if desempenho.empty or daily.empty:
        return pd.DataFrame(columns=["manager", "label", "package", "package_label",
                                     "downloads_year", "speedup_geo", "speedup_min",
                                     "speedup_max", "n_cells", "shared_package"])
    ano = window_total(daily, year_days, until)
    compartilhado = Counter(PACKAGE_OF_MANAGER.values())

    rows = []
    for row in desempenho.to_dict("records"):
        manager = row["manager"]
        package = PACKAGE_OF_MANAGER.get(manager)
        if package is None or package not in set(daily["package"]):
            continue
        rows.append({
            **row,
            "label": MANAGERS[manager]["label"],
            "package": package,
            "package_label": PACKAGE_LABELS[package],
            "downloads_year": int(ano.get(package, 0)),
            # verdadeiro quando o pacote não distingue este tratamento de outro (os 2 linkers
            # do Berry): os pontos ficam empilhados no mesmo x e isso precisa ser dito
            "shared_package": compartilhado[package] > 1,
        })
    return pd.DataFrame(rows)
