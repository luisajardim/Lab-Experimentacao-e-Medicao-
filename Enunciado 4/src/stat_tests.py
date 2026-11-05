"""Testes de correlação de Pearson e Spearman.

Calcula, em lote, o coeficiente, a estatística t e o p-valor bicaudal (t com
n − 2 g.l.) de cada teste; Spearman é o Pearson sobre os postos (empates por
posto médio). Também aplica os dois testes a um conjunto simulado, com texto de
interpretação. A aplicação aos dados reais (tamanho do efeito e IC 95%) é da T11.

Amostra em que X ou Y é constante (ex.: nenhum defeito na S-real-n10) não tem
coeficiente definido: o resultado é NaN, como no SciPy, e `p < α` dá falso, ou
seja, a réplica conta como "não rejeita H₀". Com |r| = 1, t = ±∞ e p = 0.

Issues: #79 (T05), #86 (T11).
"""

from dataclasses import dataclass
from typing import NamedTuple

import numpy as np
from scipy import stats

from config import DEFAULT_ALPHA, SEED
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
