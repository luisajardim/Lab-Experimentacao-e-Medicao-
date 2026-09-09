# Experimento Empírico: Impacto de LLMs na Produtividade e Qualidade de Código (Katas JS)

Este repositório contém a infraestrutura, execução e análise estatística de um experimento empírico comparativo do tipo **Crossover Within-Subject**, cujo objetivo é avaliar o impacto do uso de Grandes Modelos de Linguagem (LLMs) no desenvolvimento de software.

---

## 📌 Visão Geral do Experimento

* **Objeto de Estudo:** Resolução de Katas de programação em **JavaScript (Node.js)**.
* **Tratamentos:**
  1. **SEM_IA:** Resolução manual pelo desenvolvedor em ambiente controlado.
  2. **COM_IA:** Resolução com suporte de LLM (fornecendo apenas o enunciado da questão como prompt).
* **Time-box:** **25 minutos** por *trial* (otimizado para manter o foco e evitar fadiga).
* **Suíte de Aceite:** Testes unitários automatizados (Jest) mantidos fixos e isolados como critério de aceite (*time-to-green*).
* **Katas Selecionados:**
  * `kata-01-fizzbuzz`
  * `kata-02-roman-numerals`
  * `kata-03-string-calculator`
  * `kata-04-bowling-game`
  * `kata-05-isbn-validator`
  * `kata-06-pagination`

---

## 🎯 Racional de Seleção dos Katas (Metodologia Mista)

Para garantir validade interna e externa ao estudo, os 6 Katas foram divididos em duas categorias intencionais:

### 1. Desafios Clássicos e Acadêmicos (Katas 01 a 04)
* **Exemplos:** *FizzBuzz*, *Roman Numerals*, *String Calculator*, *Bowling Game*.
* **Motivação:** Trata-se de problemas amplamente difundidos na literatura técnica de TDD e maratona de programação. Eles servem como **linha de base (baseline)** para medir o comportamento e o teto de desempenho da IA em tarefas cujos padrões algorítmicos estão fortemente presentes em seus dados de treinamento.

### 2. Desafios Práticos e Não Indexados (Katas 05 e 06)
* **Exemplos:** *ISBN-10 Validator* e *Array Chunking & Pagination*.
* **Motivação:** Formulado sem dependência de plataformas competitivas públicas (como LeetCode, HackerRank ou Beecrowd). Esses katas simulam cenários rotineiros de desenvolvimento web/backend (parsing de payloads, regras formais de validação, manipulação de ponteiros/índices e paginação de dados).
* **Objetivo Experimental:** Avaliar a capacidade de generalização da LLM em problemas práticos do dia a dia, testando se ela introduz erros sutis de lógica (como problemas de *off-by-one* ou falta de tratamento de caracteres especiais) quando não há um gabarito algorítmico exato decorado.

---

## 🔬 Questões de Pesquisa (RQs) & Hipóteses

* **RQ1 (Tempo de Desenvolvimento):** O uso de IA reduz o tempo necessário para atingir o estado *Green* (*Time-to-Green*)?
* **RQ2 (Taxa de Sucesso):** O uso de IA aumenta a probabilidade de concluir o Kata dentro do limite de 25 minutos?
* **RQ3 (Qualidade do Código):** O código gerado/auxiliado por IA apresenta métricas de complexidade e duplicação equivalentes ou superiores ao código manual?

---

## ⚙️ Regras do Ambiente Controlado & Acordos do Time

1. **Escopo da IA:** A LLM terá acesso **exclusivamente ao enunciado textual** do Kata.
   * ❌ Proibido: Dar acesso à suíte de testes (`*.test.js`), usar agentes autônomos que leiam o repositório inteiro ou colar erros de compilação sem intervenção manual.
2. **Transcrição Obrigatória:** Em todos os *trials* do tratamento `COM_IA`, o desenvolvedor deve registrar o histórico/recorte do chat com a LLM em um arquivo `prompts.md` na pasta do seu trial.
3. **Uso de Ferramentas Únicas:** Uma única LLM será padronizada para todo o experimento no tratamento `COM_IA`.
4. **Crossover sem Aprendizado:** Nenhum desenvolvedor resolverá o mesmo Kata duas vezes. Cada membro resolverá Katas distintos com e sem IA para evitar contaminação por efeito de aprendizado.
5. **Automação Estrita:** Todo o tempo e execução de testes são gerenciados via CLI (`tools/timer-cli.js`).
6. **Rastreabilidade GitHub:** Cada *trial* executado por cada desenvolvedor corresponde a uma **Issue individual** no GitHub Projects e deve ser encerrado via commit.

---

## 🔀 Matriz Experimental (Crossover Design Completo)

Serão executados **12 trials no total** (3 Desenvolvedores × 4 Katas cada), garantindo que **todos os 6 Katas sejam avaliados sob ambos os tratamentos (`COM_IA` e `SEM_IA`)**:

| Kata / Exercício | Categoria | Dev 1 | Dev 2 | Dev 3 |
| :--- | :--- | :---: | :---: | :---: |
| **Kata 01: FizzBuzz** | Clássico / Baseline | — | **COM_IA** | **SEM_IA** |
| **Kata 02: Roman Numerals** | Clássico / Algorítmico | — | **SEM_IA** | **COM_IA** |
| **Kata 03: String Calculator** | Clássico / Parsing | **COM_IA** | — | **SEM_IA** |
| **Kata 04: Bowling Game** | Clássico / Regra de Negócio | **SEM_IA** | **COM_IA** | — |
| **Kata 05: ISBN-10 Validator** | Prático / Validação | **SEM_IA** | — | **COM_IA** |
| **Kata 06: Pagination** | Prático / Estrutura Web | **COM_IA** | **SEM_IA** | — |
| **Total de Issues por Dev** | | **4 Issues** | **4 Issues** | **4 Issues** |

---

## 📂 Estrutura de Pastas do Repositório

```text
Enunciado 2/
├── index.html                  # Apresentação web / Enunciado visual
├── README.md                   # Documentação principal do experimento
├── package.json                # Dependências gerais do projeto (Jest, jscpd, escomplex)
│
├── tools/                      # Ferramentas de medição (Sprint 1)
│   ├── timer-cli.js            # [Dev 1] CLI de cronometragem e runner interativo
│   └── metrics-runner.js       # [Dev 2] Runner de métricas estáticas (LOC, Complexidade, Duplicação)
│
├── katas/                      # Boilerplates dos Katas (Sprint 1 - Dev 3)
│   ├── kata-01-fizzbuzz/
│   │   ├── readme.md           # Enunciado limpo do Kata (prompt para LLM)
│   │   ├── index.js            # Assinatura base da função/classe
│   │   └── index.test.js       # Suíte fixa de testes de aceite
│   ├── kata-02-roman-numerals/
│   ├── kata-03-string-calculator/
│   ├── kata-04-bowling-game/
│   ├── kata-05-isbn-validator/ # Kata focado em parsing/validação de regras
│   └── kata-06-pagination/     # Kata focado em estrutura de dados/fórmulas de índice
│
├── trials/                     # Execuções individuais dos trials (Sprint 2)
│   ├── dev1/
│   │   ├── kata-01-sem-ia/
│   │   │   ├── index.js        # Código final implementado
│   │   │   └── metrics.json    # Métricas estáticas do trial
│   │   └── kata-03-com-ia/
│   │       ├── index.js        # Código final gerado
│   │       ├── prompts.md      # Histórico de conversas com a LLM
│   │       └── metrics.json
│   ├── dev2/
│   └── dev3/
│
├── data/                       # Logs consolidados
│   └── trials-log.json         # Registro bruto do timer-cli (tempos, tentativas, sucessos)
│
└── analysis/                   # Pipelines de Análise Estatística (Sprint 3)
    ├── stats_wilcoxon.py       # [Dev 1] Teste de Wilcoxon e estatística descritiva (RQ1, RQ2)
    ├── code_quality.py         # [Dev 2] Análise de qualidade de código (RQ3)
    ├── charts_generator.py     # [Dev 3] Geração automatizada de gráficos e Boxplots
    └── outputs/                # Imagens e gráficos gerados para o relatório final

```

---

## 📅 Divisão de Tarefas por Sprint & Atribuições dos Devs

### **Sprint 1: Preparação e Ferramental**

* **Dev 1:** Desenvolvimento do `tools/timer-cli.js` (cronometragem CLI, captura de `Shift + T`, execução do Jest via subprocesso e geração de `data/trials-log.json`).
* **Dev 2:** Desenvolvimento do `tools/metrics-runner.js` (integração de analisadores JS para extração de LOC, complexidade ciclomática e duplicação).
* **Dev 3:** Criação e validação dos Katas em `katas/` com boilerplates em JS e suítes de teste Jest completas.

### **Sprint 2: Execução dos Trials**

* Execução individual das 4 Issues por dev conforme a matriz Crossover.
* Uso obrigatório do `timer-cli.js` durante cada *trial*.
* Armazenamento das transcrições de prompts e soluções em `trials/devX/`.

### **Sprint 3: Análise Estatística & Visualização**

* **Dev 1:** Script em Python (`stats_wilcoxon.py`) para aplicação do **Teste de Wilcoxon Signed-Rank** nos dados brutos de tempo.
* **Dev 2:** Script em Python (`code_quality.py`) para sumarização e comparação das métricas estáticas do código.
* **Dev 3:** Script em Python (`charts_generator.py`) para renderização dos gráficos finais (Boxplots e Histogramas).

---

## 🚀 Como Executar o Timer-CLI de um Trial

1. Instale as dependências:

```bash
npm install

```

2. Inicie o trial indicando o dev, kata, tratamento e comando do teste:

```bash
npm run timer -- \
  --dev dev1 \
  --kata kata-05-isbn-validator \
  --treatment COM_IA \
  --cmd "npx jest katas/kata-05-isbn-validator" \
  --timebox 25

```

3. Durante o trial:

* Pressione **`Shift + T`** para rodar a suíte de testes de aceite.
* O relógio irá parar automaticamente no primeiro evento de sucesso (*Green*) ou ao esgotar o limite configurado (*Timeout*).