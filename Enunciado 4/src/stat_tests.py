"""Testes de correlação de Pearson e Spearman.

Calcula, em lote, o coeficiente, a estatística t e o p-valor bicaudal (t com
n − 2 g.l.) de cada teste; Spearman é o Pearson sobre os postos (empates por
posto médio). Também aplica os dois testes a um conjunto simulado, com texto de
interpretação, e à amostra real de 30 classes do KC1, com tamanho do efeito e IC 95%
(Fisher z para r; bootstrap BCa para ρₛ) e comentário sobre a importância prática.

Amostra em que X ou Y é constante (ex.: nenhum defeito na S-real-n10) não tem
coeficiente definido: o resultado é NaN, como no SciPy, e `p < α` dá falso, ou
seja, a réplica conta como "não rejeita H₀". Com |r| = 1, t = ±∞ e p = 0.

Issues: #79 (T05), #86 (T11).
"""

from dataclasses import dataclass
from functools import cache
from typing import NamedTuple

import numpy as np
import pandas as pd
from scipy import stats

from config import DEFAULT_ALPHA, SEED
from data import SAMPLE_CSV
from generate import generate

# Exemplo da seção 3 do dashboard: efeito intermediário da grade, com H₀ falsa.
EXAMPLE_SITUATION = "S-real"
EXAMPLE_RHO = 0.3


class CorrelationResult(NamedTuple):
    """Resultado de um teste; `coef`, `t` e `p` têm o formato do lote ([reps] ou escalar)."""

    coef: np.ndarray
    t: np.ndarray
    p: np.ndarray
    df: int


@dataclass(frozen=True)
class Example:
    """Os dois testes aplicados a um único conjunto simulado."""

    situation: str
    rho: float
    n: int
    x: np.ndarray
    y: np.ndarray
    pearson: CorrelationResult
    spearman: CorrelationResult


def _validate(x, y) -> tuple[np.ndarray, np.ndarray]:
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.shape != y.shape:
        raise ValueError(f"x e y precisam ter o mesmo formato: {x.shape} × {y.shape}")
    if x.ndim == 0 or x.shape[-1] < 3:
        raise ValueError(f"São necessárias ao menos 3 observações (n − 2 g.l.); formato {x.shape}")
    return x, y


def _correlation(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """r de Pearson ao longo do último eixo; NaN onde X ou Y é constante."""
    dx = x - x.mean(axis=-1, keepdims=True)
    dy = y - y.mean(axis=-1, keepdims=True)
    # A checagem exata evita que o resíduo de arredondamento de uma coluna constante vire r.
    constant = (x.max(axis=-1) == x.min(axis=-1)) | (y.max(axis=-1) == y.min(axis=-1))
    with np.errstate(divide="ignore", invalid="ignore"):
        r = (dx * dy).sum(axis=-1) / np.sqrt((dx * dx).sum(axis=-1) * (dy * dy).sum(axis=-1))
    # Arredondamentos podem dar |r| levemente acima de 1.
    return np.where(constant, np.nan, np.clip(r, -1.0, 1.0))


def _t_test(r: np.ndarray, n: int) -> CorrelationResult:
    """t = r·√((n−2)/(1−r²)) e p bicaudal pela t com n − 2 g.l."""
    df = n - 2
    with np.errstate(divide="ignore", invalid="ignore"):
        t = r * np.sqrt(df / (1 - r**2))
    p = 2 * stats.t.sf(np.abs(t), df)
    # `[()]` devolve escalares quando a entrada é uma única amostra.
    return CorrelationResult(r[()], t[()], p[()], df)


def pearson(x, y) -> CorrelationResult:
    """Teste de Pearson. `x` e `y`: formato [n] ou [reps, n] (o último eixo é a amostra)."""
    x, y = _validate(x, y)
    return _t_test(_correlation(x, y), x.shape[-1])


def spearman(x, y) -> CorrelationResult:
    """Teste de Spearman: Pearson sobre os postos, com posto médio nos empates."""
    x, y = _validate(x, y)
    ranks_x = stats.rankdata(x, method="average", axis=-1)
    ranks_y = stats.rankdata(y, method="average", axis=-1)
    return _t_test(_correlation(ranks_x, ranks_y), x.shape[-1])


def run_example(
    situation: str = EXAMPLE_SITUATION, rho: float = EXAMPLE_RHO, seed: int = SEED
) -> Example:
    """Gera um único conjunto simulado e aplica os dois testes."""
    x, y = generate(situation, rho, reps=1, rng=np.random.default_rng(seed))
    x, y = x[0], y[0]
    return Example(situation, rho, x.size, x, y, pearson(x, y), spearman(x, y))


def _number(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def _p_text(p: float) -> str:
    return "p < 0,001" if p < 0.001 else f"p = {_number(p)}"


def _decision_text(name: str, coef_symbol: str, result: CorrelationResult, alpha: float) -> str:
    decision = "rejeita H₀" if result.p < alpha else "não rejeita H₀"
    return (
        f"**{name}:** {coef_symbol} = {_number(result.coef)}, t({result.df}) = "
        f"{_number(result.t, 2)}, {_p_text(result.p)}: {decision} com α = {_number(alpha, 2)}."
    )


def _truth_text(rho: float, pearson_rejects: bool, spearman_rejects: bool) -> str:
    """O que cada decisão significa, já que na simulação sabemos se H₀ é verdadeira."""
    h0_true = rho == 0
    error = "erro tipo I" if h0_true else "erro tipo II"
    premise = (
        "Aqui sabemos que H₀ é verdadeira (ρ latente = 0)"
        if h0_true
        else f"Aqui sabemos que H₀ é falsa (ρ latente = {_number(rho, 1)})"
    )
    # Com H₀ verdadeira, acerta quem não rejeita; com H₀ falsa, quem rejeita.
    pearson_right, spearman_right = pearson_rejects != h0_true, spearman_rejects != h0_true
    if pearson_right and spearman_right:
        return f"{premise}, então os dois testes acertam"
    if not pearson_right and not spearman_right:
        return f"{premise}, então os dois testes cometem {error} nesta amostra"
    right, wrong = ("Pearson", "Spearman") if pearson_right else ("Spearman", "Pearson")
    return f"{premise}, então o {right} acerta e o {wrong} comete {error} nesta amostra"


def interpret_example(example: Example, alpha: float = DEFAULT_ALPHA) -> str:
    """Texto de interpretação (Markdown), montado a partir dos valores calculados."""
    r_test, rho_test = example.pearson, example.spearman
    if np.isnan(r_test.coef) or np.isnan(rho_test.coef):
        raise ValueError("Amostra constante: os coeficientes não estão definidos.")
    pearson_rejects, spearman_rejects = bool(r_test.p < alpha), bool(rho_test.p < alpha)

    if pearson_rejects and spearman_rejects:
        agreement = "Os dois testes indicam associação entre tamanho da classe e defeitos."
    elif spearman_rejects:
        agreement = (
            "Só o Spearman indica associação: a tendência aparece nos postos, mas a variabilidade "
            "dos valores (classes muito grandes, muitos zeros) não deixa o Pearson detectá-la "
            "nesta amostra."
        )
    elif pearson_rejects:
        agreement = (
            "Só o Pearson indica associação: o resultado depende dos valores, e pode vir de "
            "poucas classes extremas, sem uma tendência geral nos postos."
        )
    else:
        agreement = "Nenhum dos dois testes encontra evidência de associação nesta amostra."

    truth = _truth_text(example.rho, pearson_rejects, spearman_rejects)

    return "\n\n".join(
        [
            f"{_decision_text('Pearson', 'r', r_test, alpha)}  \n"
            f"{_decision_text('Spearman', 'ρₛ', rho_test, alpha)}",
            f"{agreement} {truth}. O p-valor é a probabilidade de obter um |t| tão ou mais extremo "
            "que o observado **se H₀ fosse verdadeira**; não é a probabilidade de H₀ ser "
            "verdadeira.",
            f"É um único conjunto ({example.situation}, n = {example.n}): ele mostra como ler o "
            "resultado, mas não diz qual teste é melhor. Isso depende da taxa de rejeição em "
            "muitas réplicas (seções 4 e 5).",
        ]
    )


# --- Dados reais (T11, #86) ---------------------------------------------------

CONFIDENCE = 0.95
BOOTSTRAP_RESAMPLES = 10_000
# Cohen (1988), para |r| ou |ρₛ|: limite inferior de cada faixa.
COHEN_LABELS = ((0.5, "grande"), (0.3, "moderado"), (0.1, "pequeno"), (0.0, "desprezível"))


@dataclass(frozen=True)
class RealAnalysis:
    """Os dois testes na amostra real, com IC 95%, a classe mais influente e números práticos."""

    n: int
    pearson: CorrelationResult
    spearman: CorrelationResult
    pearson_ci: tuple[float, float]  # Fisher z
    spearman_ci: tuple[float, float]  # bootstrap BCa
    pearson_bootstrap_ci: tuple[float, float]  # só para comparar com o Fisher
    influential_loc: float
    influential_defects: float
    r_without_influential: float
    rho_s_without_influential: float
    total_defects: float
    share_defects_larger_half: float
    any_defect_larger_half: float
    any_defect_smaller_half: float


def cohen_label(coef: float) -> str:
    return next(label for low, label in COHEN_LABELS if abs(coef) >= low)


def fisher_ci(r: float, n: int, confidence: float = CONFIDENCE) -> tuple[float, float]:
    """IC de r pela transformação z de Fisher (supõe normalidade bivariada)."""
    half = stats.norm.ppf((1 + confidence) / 2) / np.sqrt(n - 3)
    z = np.arctanh(r)
    return float(np.tanh(z - half)), float(np.tanh(z + half))


def bootstrap_ci(x, y, test=None, n_resamples: int = BOOTSTRAP_RESAMPLES, seed: int = SEED,
                 confidence: float = CONFIDENCE) -> tuple[float, float]:
    """IC bootstrap BCa do coeficiente de `test` (Spearman por padrão), reamostrando pares."""
    test = spearman if test is None else test

    def statistic(a, b, axis):
        return test(np.moveaxis(a, axis, -1), np.moveaxis(b, axis, -1)).coef

    result = stats.bootstrap(
        (np.asarray(x, dtype=float), np.asarray(y, dtype=float)),
        statistic,
        paired=True,
        vectorized=True,
        method="BCa",
        n_resamples=n_resamples,
        confidence_level=confidence,
        rng=np.random.default_rng(seed),
    )
    return float(result.confidence_interval.low), float(result.confidence_interval.high)


def analyze_real(x, y) -> RealAnalysis:
    x, y = _validate(x, y)
    n = x.size
    r_test, s_test = pearson(x, y), spearman(x, y)

    # Classe mais influente: a que mais muda o r quando é retirada (leave-one-out em lote).
    without = np.array([np.delete(np.arange(n), i) for i in range(n)])  # linha i: todas menos i
    x_loo, y_loo = x[without], y[without]
    r_loo = pearson(x_loo, y_loo).coef
    i = int(np.nanargmax(np.abs(r_loo - r_test.coef)))

    larger = x > np.median(x)
    return RealAnalysis(
        n=n,
        pearson=r_test,
        spearman=s_test,
        pearson_ci=fisher_ci(float(r_test.coef), n),
        spearman_ci=bootstrap_ci(x, y, spearman),
        pearson_bootstrap_ci=bootstrap_ci(x, y, pearson),
        influential_loc=float(x[i]),
        influential_defects=float(y[i]),
        r_without_influential=float(r_loo[i]),
        rho_s_without_influential=float(spearman(x_loo[i], y_loo[i]).coef),
        total_defects=float(y.sum()),
        share_defects_larger_half=float(y[larger].sum() / y.sum()),
        any_defect_larger_half=float((y[larger] > 0).mean()),
        any_defect_smaller_half=float((y[~larger] > 0).mean()),
    )


@cache
def real_sample_analysis() -> RealAnalysis:
    """Análise da amostra de 30 classes do KC1 (`data/real/kc1_sample30.csv`)."""
    sample = pd.read_csv(SAMPLE_CSV)
    return analyze_real(sample["loc"], sample["defects"])


def _pct(value: float) -> str:
    return f"{100 * value:.0f}%"


def _interval(ci: tuple[float, float]) -> str:
    return f"[{_number(ci[0], 2)}; {_number(ci[1], 2)}]"


def real_data_table(analysis: RealAnalysis | None = None, alpha: float = DEFAULT_ALPHA
                    ) -> pd.DataFrame:
    """Tabela da seção 6: estatística, t, p, tamanho do efeito com IC 95% e conclusão."""
    analysis = real_sample_analysis() if analysis is None else analysis
    rows = []
    for name, symbol, result, ci, method, kind in (
        ("Pearson", "r", analysis.pearson, analysis.pearson_ci, "Fisher z", "linear"),
        ("Spearman", "ρₛ", analysis.spearman, analysis.spearman_ci,
         f"bootstrap BCa ({BOOTSTRAP_RESAMPLES:,} reamostragens)".replace(",", "."), "monotônica"),
    ):
        rejects = result.p < alpha
        rows.append(
            {
                "Teste": name,
                "Estatística": f"{symbol} = {_number(result.coef, 2)}",
                f"t ({result.df} g.l.)": _number(result.t, 2),
                "p-valor": _p_text(result.p).removeprefix("p = ").removeprefix("p "),
                "Tamanho do efeito (IC 95%)": f"{_number(result.coef, 2)} {_interval(ci)} · "
                f"{cohen_label(result.coef)}",
                "Método do IC": method,
                f"Conclusão (α = {_number(alpha, 2)})": (
                    f"Rejeita H₀: há associação {kind} entre LOC e defeitos"
                    if rejects
                    else "Não rejeita H₀: sem evidência de associação"
                ),
            }
        )
    return pd.DataFrame(rows)


def real_data_text(analysis: RealAnalysis | None = None, alpha: float = DEFAULT_ALPHA) -> str:
    """Comentário da seção 6 (Markdown): mesma conclusão?, importância prática e ressalvas."""
    a = real_sample_analysis() if analysis is None else analysis
    pearson_rejects, spearman_rejects = bool(a.pearson.p < alpha), bool(a.spearman.p < alpha)
    if pearson_rejects == spearman_rejects:
        verdict = "rejeitam" if pearson_rejects else "não rejeitam"
        same = (
            f"**Mesma conclusão.** Com α = {_number(alpha, 2)}, os dois testes {verdict} H₀ "
            f"na amostra de {a.n} classes."
        )
    else:
        winner = "Pearson" if pearson_rejects else "Spearman"
        same = (
            f"**Conclusões diferentes.** Com α = {_number(alpha, 2)}, só o {winner} rejeita H₀ "
            f"na amostra de {a.n} classes."
        )
    low, high = a.spearman_ci
    giant = (
        f"{a.influential_loc:,.0f} LOC e {a.influential_defects:,.0f} defeitos".replace(",", ".")
    )
    paragraphs = [
        same,
        "**Tamanho do efeito.** O ρₛ = "
        f"{_number(a.spearman.coef, 2)} é um efeito {cohen_label(a.spearman.coef)} pelos critérios "
        f"de Cohen, mas o IC 95% vai de {_number(low, 2)} ({cohen_label(low)}) a "
        f"{_number(high, 2)} ({cohen_label(high)}): com 30 classes, a associação é clara, mas o "
        "tamanho dela ainda é incerto.",
        "**Importância prática.** Na amostra, a metade das classes com mais LOC concentra "
        f"{_pct(a.share_defects_larger_half)} dos defeitos (sozinha, a classe de {giant} responde "
        f"por {_pct(a.influential_defects / a.total_defects)}), e "
        f"{_pct(a.any_defect_larger_half)} delas têm algum defeito, contra "
        f"{_pct(a.any_defect_smaller_half)} na metade menor. Para quem decide onde revisar ou testar "
        "primeiro, o tamanho da classe é um critério útil: olhar as classes maiores encontra a "
        "maior parte dos defeitos. Ele não substitui uma análise caso a caso: "
        f"{_pct(1 - a.any_defect_larger_half)} das classes da metade maior não têm defeito nenhum.",
        "**Por que confiar mais no Spearman aqui.** O r = "
        f"{_number(a.pearson.coef, 2)} é inflado por uma única classe ({giant}): sem ela, o r cai "
        f"para {_number(a.r_without_influential, 2)} e o ρₛ fica em "
        f"{_number(a.rho_s_without_influential, 2)}. O IC de Fisher "
        f"{_interval(a.pearson_ci)} também é estreito demais, porque supõe dados normais; um "
        f"bootstrap do próprio r dá {_interval(a.pearson_bootstrap_ci)}. É o mesmo padrão da "
        "simulação (seções 4 e 5): nesses dados, o Spearman descreve melhor a tendência geral.",
    ]
    return "\n\n".join(paragraphs)
