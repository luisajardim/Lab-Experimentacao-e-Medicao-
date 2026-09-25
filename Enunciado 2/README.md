# Experimento Empírico: Impacto de LLMs na Produtividade e Qualidade de Código (Katas JS)

Este sub-repositório reúne a infraestrutura, a execução e a análise final do experimento comparativo entre resolução manual e resolução com suporte de IA em katas de programação JavaScript.

O projeto foi concluído e os artefatos finais — relatório, dados coletados, métricas estáticas e gráficos de análise — ficaram disponíveis no próprio repositório.

---

## ✅ Status do Projeto

O estudo foi finalizado com:

- 12 trials executados no total;
- 6 trials com IA (`COM_IA`);
- 6 trials sem IA (`SEM_IA`);
- 11 sucessos e 1 timeout;
- análise estatística e geração de gráficos automatizados;
- relatório consolidado em [RELATORIO.md](RELATORIO.md).

---

## 🎯 Objetivo

Avaliar, em condições controladas, o impacto do uso de LLMs na resolução de katas de programação em JavaScript, comparando:

1. `SEM_IA`: desenvolvimento manual;
2. `COM_IA`: desenvolvimento com auxílio de IA, usando apenas o enunciado do kata como entrada.

As questões centrais do experimento foram:

- RQ1: O uso de IA reduz o tempo para atingir o estado Green?
- RQ2: O uso de IA aumenta a taxa de sucesso dentro do timebox?
- RQ3: O código gerado com IA apresenta qualidade estrutural equivalente ou superior ao código manual?

---

## 🔬 Metodologia

### Katas utilizados

- FizzBuzz
- Roman Numerals
- String Calculator
- Bowling Game
- ISBN-10 Validator
- Array Chunking & Pagination

### Condições do experimento

- Timebox de 25 minutos por trial;
- suíte fixa de testes automatizados como critério de aceite;
- acesso da IA restrito ao enunciado do kata;
- registro de tempo, tentativas e sucesso por trial;
- coleta de métricas estáticas de código por solução final.

### Resultado principal observado

Os dados finais mostram que:

- a mediana de tempo com IA foi de aproximadamente 22,5 segundos;
- a mediana de tempo sem IA foi de aproximadamente 846,5 segundos;
- a taxa de sucesso com IA foi de 100% (`6/6`);
- a taxa de sucesso sem IA foi de 83,3% (`5/6`);
- todas as soluções com IA alcançaram Green em 1 tentativa;
- o único timeout ocorreu no tratamento manual (`Bowling Game`).

Esses resultados indicam uma vantagem clara do tratamento com IA no contexto do experimento, ainda que com ressalvas sobre o tamanho amostral e a natureza exploratória da análise.

---

## 📂 Estrutura do Repositório

```text
Enunciado 2/
├── README.md
├── RELATORIO.md
├── APRESENTACAO.md
├── package.json
├── index.html
├── tools/
│   ├── timer-cli.js
│   ├── metrics-runner.js
│   ├── finish-trial.js
│   └── ...
├── katas/
│   ├── kata-00-teste-string-transformer/
│   ├── kata-01-fizzbuzz/
│   ├── kata-02-roman-numerals/
│   ├── kata-03-string-calculator/
│   ├── kata-04-bowling-game/
│   ├── kata-05-isbn-10-validator/
│   └── kata-06-array-chunking-pagination/
├── trials/
│   ├── alvimdev/
│   ├── luisajardim/
│   └── pedroseabra27/
├── data/
│   └── trials-log.json
├── analysis/
│   ├── charts_generator.py
│   ├── code_quality.py
│   ├── inferential_stats.py
│   ├── pyproject.toml
│   ├── charts/
│   └── output/
│       ├── charts/
│       ├── code_quality_comparison.csv
│       ├── code_quality_summary.json
│       ├── monte_carlo_simulations.csv
│       └── stats_summary.json
└── node_modules/
```

---

## 🧪 Como executar e reproduzir

### 1. Instalar dependências do projeto

```bash
npm install
```

### 2. Rodar um trial manualmente

```bash
npm run timer -- \
  --dev luisajardim \
  --kata kata-05-isbn-10-validator \
  --treatment COM_IA \
  --cmd "npx jest katas/kata-05-isbn-10-validator" \
  --timebox 25
```

Durante o trial, a tecla `Shift + T` executa a suíte de testes e o relógio encerra automaticamente no primeiro Green ou no timeout.

### 3. Extrair métricas estáticas

```bash
npm run metrics
```

### 4. Executar a análise estatística e gráficos

```bash
cd analysis
python -m venv .venv
. .venv/bin/activate
pip install .
python charts_generator.py
python inferential_stats.py
```

---

## 📊 Artefatos finais de análise

Os resultados finais estão disponíveis em:

- [RELATORIO.md](RELATORIO.md)
- [APRESENTACAO.md](APRESENTACAO.md)
- [data/trials-log.json](data/trials-log.json)
- [analysis/output/stats_summary.json](analysis/output/stats_summary.json)
- [analysis/output/code_quality_summary.json](analysis/output/code_quality_summary.json)
- [analysis/output/charts](analysis/output/charts)

A pasta [analysis/output/charts](analysis/output/charts) contém os gráficos gerados para as RQs, incluindo:

- `rq1_tempo_por_kata.png`
- `rq1_diferenca_tempo.png`
- `rq2_taxa_sucesso.png`
- `rq2_tentativas_stripplot.png`
- `rq3_metricas_distribuicao.png`
- `rq3_perfil_radar.png`
- `rq3_efeitos_metricas.png`
- `monte_carlo_distribuicoes.png`

---

## 🧩 Observações finais

Este projeto foi entregue como um experimento empírico completo, com infraestrutura de coleta, rastreabilidade de trials, análise estatística e produção de resultados. Ele serve como base reprodutível para estudos posteriores sobre produtividade, qualidade estrutural e uso de IA em software.

A principal conclusão do laboratório é que, nas condições avaliadas, o uso de IA foi associado a:

- menor tempo para atingir Green;
- maior taxa de sucesso;
- menor número de tentativas até a solução final;
- qualidade estrutural equivalente ou melhor, conforme as métricas observadas.

---

## 📌 Referências e tecnologias

- Node.js
- Jest
- escomplex
- jscpd
- Python 3.10+
- pandas, NumPy, SciPy, Matplotlib, Seaborn
