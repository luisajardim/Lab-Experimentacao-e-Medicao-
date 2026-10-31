# Cenário — Pearson × Spearman (par P5)

## Pergunta

> Em um sistema C++ da NASA, classes maiores tendem a ter mais defeitos de modo geral, ou a associação
> observada é puxada por poucas classes gigantes?

- **X**: tamanho da classe, em linhas de código (`loc`).
- **Y**: número de defeitos registrados para a classe (`defects`).
- Dados reais: NASA KC1 por classe, 145 classes; amostra de 30 para a aplicação final (ver [fonte_dados.md](fonte_dados.md)).

## Hipóteses

| | Em símbolos | Em palavras |
|---|---|---|
| **H₀** | ρ = 0 | O tamanho da classe não está associado ao número de defeitos. |
| **H₁** | ρ ≠ 0 | O tamanho da classe está associado ao número de defeitos (para mais ou para menos). |

- **Bicaudal**, α = 0,05 (o dashboard também mostra α = 0,01). O grupo espera ρ > 0, mas não usa essa
  direção no teste: o bicaudal é o padrão, é mais conservador e não depende de uma aposta feita sobre os dados.
- No Pearson, ρ é a correlação linear entre os valores; no Spearman, é a correlação entre os postos
  (associação monotônica).

## Como cada teste responde à pergunta

- **Pearson** trabalha com os valores. Uma classe gigante com muitos defeitos pesa muito no cálculo, então um r
  alto pode vir de poucas classes extremas.
- **Spearman** trabalha com os postos. Cada classe pesa igual, então o ρ mede a tendência geral
  ("classes maiores costumam ter mais defeitos").
- Se o Pearson indicar uma associação bem mais forte que o Spearman, é sinal de que valores extremos estão
  puxando o resultado. No KC1 inteiro, r = 0,69 e ρ = 0,57.

## Como os dados da simulação são gerados

Quatro situações. Em todas, o tamanho do efeito é o **ρ latente** ∈ {0; 0,1; 0,2; 0,3; 0,4; 0,5; 0,6}, com
**10.000 réplicas** por combinação (margem de Monte Carlo ≈ ±0,43 pp em torno de 5%). Com ρ = 0, X e Y são
independentes nas três primeiras situações, então H₀ é verdadeira para os dois testes. Na S-outlier, ρ = 0
significa que não há relação entre as classes comuns; qualquer rejeição vem só das classes extremas.

| Situação | Geração | n | Por quê |
|---|---|---|---|
| **S-base** | Normal bivariada padronizada (médias 0, desvios 1, correlação ρ) | 30 | Caso ideal para o Pearson. Os dois testes não mudam com mudança de escala, então média e desvio não alteram nada. |
| **S-real** | Cópula gaussiana: Z ~ N₂(0, ρ) → U = Φ(Z) → LOC = Gamma⁻¹(U₁) e defeitos = BinNeg⁻¹(U₂) | 30 | Reproduz a forma dos dados reais (assimetria, classes gigantes, muitos zeros), que viola os pressupostos do Pearson. |
| **S-real-n10** | Mesmo gerador da S-real | 10 | Violação por amostra pequena. |
| **S-outlier** | S-real em que cada classe tem chance de 1 em 145 de ser trocada por uma classe extrema: LOC e defeitos sorteados acima do percentil 99 das distribuições ajustadas (≥ 1.770 LOC e ≥ 57 defeitos) | 30 | Violação por outlier, e o fenômeno da pergunta. Cerca de 19% das amostras recebem uma classe extrema. |

A cópula gaussiana mantém exatamente as distribuições ajustadas de cada variável e controla a dependência
entre elas só pelo ρ latente.

### Por que a S-outlier existe

A S-outlier foi acrescentada em 31/10/2026, depois de testarmos o gerador. Ao comparar as correlações geradas
com as do KC1, vimos que a cópula gaussiana não reproduz o que acontece nos dados reais:

| | r (Pearson) | ρ (Spearman) |
|---|---|---|
| Gerador S-real, ρ latente = 0,6 (amostra enorme) | 0,47 | 0,52 |
| KC1 completo | 0,69 | 0,57 |
| KC1 sem a classe de 2.883 LOC e 101 defeitos | 0,57 | 0,56 |
| KC1 sem as 3 classes com mais defeitos | 0,52 | 0,55 |

No KC1, **uma única classe** sobe o r de 0,57 para 0,69, enquanto o ρ quase não muda. A proporção de classes que
estão ao mesmo tempo entre as 10% maiores e as 10% com mais defeitos é parecida no KC1 (4,8%) e no gerador
(4,1%): a diferença é um ponto dominante, que a cópula praticamente nunca produz. A S-outlier coloca esse tipo de
ponto na simulação, na mesma frequência do KC1 (1 classe extrema em 145). A classe do KC1 equivale a um extremo
de cerca de 1 em 1.000 nas distribuições ajustadas (percentil 99,9: 2.817 LOC e 108 defeitos).

### Parâmetros (ajustados no KC1 inteiro, máxima verossimilhança)

Gerados por [`src/fit.py`](../src/fit.py) (`uv run python -m fit`) e salvos em `data/real/params.json`.

**LOC ~ Gamma(forma = 0,607; escala = 487,9)**

| Percentil | 10 | 25 | 50 | 75 | 90 | 99 | Média |
|---|---|---|---|---|---|---|---|
| Real | 9 | 44 | 162 | 315 | 700 | 2.356 | 296 |
| Gamma ajustada | 9 | 44 | 157 | 402 | 769 | 1.770 | 296 |

- O LOC real é muito assimétrico à direita (assimetria 3,40, mediana 162, máximo 2.883). A forma < 1 da Gamma
  reproduz isso: muitas classes pequenas e uma cauda longa.
- **Por que não lognormal:** a lognormal ajustou mal (KS p = 0,001). O log do LOC é assimétrico para a
  esquerda (−0,83), porque 13% das classes têm até 10 LOC, e a lognormal erra a mediana (107 contra 162) e
  exagera a cauda (percentil 99 = 6.182 contra 2.356). A Gamma não é rejeitada (KS p = 0,22).

**Defeitos ~ Binomial negativa(r = 0,170; média = 4,61)** (no SciPy: `nbinom(n=r, p=r/(r+μ))`, p = 0,0354)

| | Classes sem defeito | Classes com ≥ 20 defeitos |
|---|---|---|
| Real | 58,6% | 6,9% |
| Binomial negativa ajustada | 56,8% | 7,0% |

- Contagens com muitos zeros e cauda longa (máximo 101, assimetria 5,53). A variância real (≈ 118) é 25 vezes
  a média, o que descarta a Poisson. A dispersão r = 0,17 captura esse excesso de variabilidade.

**Efeito de referência:** a correlação de escores normais do KC1 (estimativa do ρ latente da cópula) é 0,59.
Com ρ latente = 0,6, o gerador produz ρ_s ≈ 0,52 (os empates nos defeitos atenuam a correlação), um pouco abaixo
do 0,57 do KC1; então a grade de 0 a 0,6 vai de "sem efeito" até perto do efeito observado.

## Expectativa antes de simular

*Registrada em 31/10/2026, antes de rodar qualquer simulação.*

**O grupo espera que o Spearman se saia melhor na situação realista e com n = 10, e o Pearson na situação base.**

- **Erro tipo I (Q1):** os dois perto de 5% nas três situações. Com ρ = 0, X e Y são independentes, e nesse
  caso a distribuição dos dois testes sob H₀ continua aproximadamente correta, mesmo com dados assimétricos.
- **Poder na S-base (Q2):** o Pearson com um pouco mais de poder. Com dados normais, ele é o teste ótimo, e o
  Spearman precisa de cerca de 10% mais observações para o mesmo poder (eficiência relativa assintótica 9/π² ≈ 0,91).
- **Poder na S-real (Q3):** o Spearman com mais poder. Na Gamma e na binomial negativa, poucos valores extremos
  dominam a soma dos produtos que forma o r. Isso deixa o r muito variável de amostra para amostra e esconde a
  tendência geral. Os postos limitam a influência de cada classe.
- **Poder na S-real-n10 (Q3):** os dois perdem muito poder. A vantagem do Spearman deve continuar, mas menor,
  porque com 10 classes e ~57% de zeros sobram muitos empates nos postos.

**S-outlier (sem expectativa a priori).** Essa situação foi criada depois da análise exploratória descrita
acima, que já mediu o comportamento dos testes nela: com ρ = 0, o Pearson rejeitou H₀ em ~20% das amostras e o
Spearman em ~6%; com ρ = 0,3, 39% contra 31%. Por isso ela **não** entra na comparação "esperado × encontrado"
da conclusão; serve para mostrar o efeito de um ponto dominante, que é o fenômeno da pergunta.

**Evidência que embasa a expectativa:** num piloto com 2.000 subamostras de 30 classes do próprio KC1
([`scripts/piloto.py`](../scripts/piloto.py), resultado em `data/real/piloto.json`), o Spearman rejeitou H₀ em
94,5% delas e o Pearson em 84,7%, apesar de o r do dataset inteiro (0,69) ser maior que o ρ (0,57). O piloto
usa só dados reais: mostra com que frequência cada teste "vê" a associação com n = 30, mas não diz se acertou.

## Limitações do cenário

- A Gamma subestima a cauda extrema do LOC (percentil 99 = 1.770 contra 2.356), então a simulação gera um pouco
  menos classes gigantes que os dados reais. Isso tende a *favorecer* o Pearson na S-real.
- A binomial negativa superestima a proporção de classes com ≥ 50 defeitos (1,4% contra 0,7%).
- A cópula gaussiana impõe uma forma específica de dependência (simétrica, sem dependência extra nas caudas).
  Por isso, nas situações S-real e S-real-n10 o r fica abaixo do ρ, ao contrário do KC1; a S-outlier
  existe para cobrir essa diferença.
- Na S-outlier, LOC e defeitos da classe extrema são sorteados de forma independente dentro das caudas, e a
  taxa (1/145) vem de uma única classe do KC1.
- Os parâmetros vêm das 145 classes do KC1, não da amostra de 30, para ficarem mais estáveis.
