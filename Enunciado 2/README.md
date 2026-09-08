# Experimento Empírico: Impacto de LLMs na Produtividade e Qualidade de Código (Katas JS)

Este repositório contém a infraestrutura, execução e análise estatística de um experimento empírico comparativo do tipo **Crossover Within-Subject**, cujo objetivo é avaliar o impacto do uso de Grandes Modelos de Linguagem (LLMs) no desenvolvimento de software.

---

## 📌 Visão Geral do Experimento

* **Objeto de Estudo:** Resolução de Katas de programação em **JavaScript (Node.js)**.
* **Tratamentos:**
  1. **SEM_IA:** Resolução manual pelo desenvolvedor em ambiente controlado.
  2. **COM_IA:** Resolução com suporte de LLM (fornecendo apenas o enunciado da questão como prompt).
* **Time-box:** 35 minutos por *trial*.
* **Suíte de Aceite:** Testes unitários automatizados (Jest) mantidos fixos e isolados como critério de aceite (*time-to-green*).

---

## 🔬 Questões de Pesquisa (RQs) & Hipóteses

* **RQ1 (Tempo de Desenvolvimento):** O uso de IA reduz o tempo necessário para atingir o estado *Green* (*Time-to-Green*)?
* **RQ2 (Taxa de Sucesso):** O uso de IA aumenta a probabilidade de concluir o Kata dentro do limite de 35 minutos?
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

## 🔀 Matriz Experimental (Crossover Design)

Serão executados **12 trials no total** (3 Desenvolvedores × 4 Katas):

| Desenvolvedor | Kata 01 | Kata 02 | Kata 03 | Kata 04 | Total Issues |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Dev 1** | **SEM_IA** | **COM_IA** | **SEM_IA** | **COM_IA** | 4 Issues |
| **Dev 2** | **COM_IA** | **SEM_IA** | **COM_IA** | **SEM_IA** | 4 Issues |
| **Dev 3** | **SEM_IA** | **COM_IA** | **COM_IA** | **SEM_IA** | 4 Issues |

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
│   ├── kata-01-foo/
│   │   ├── README.md           # Enunciado limpo do Kata (prompt para LLM)
│   │   ├── index.js            # Assinatura base da função/classe
│   │   └── index.test.js       # Suíte fixa de testes de aceite
│   ├── kata-02-bar/
│   ├── kata-03-baz/
│   └── kata-04-qux/
│
├── trials/                     # Execuções individuais dos trials (Sprint 2)
│   ├── dev1/
│   │   ├── kata-01-sem-ia/
│   │   │   ├── index.js        # Código final implementado
│   │   │   └── metrics.json    # Métricas estáticas do trial
│   │   └── kata-02-com-ia/
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
* **Dev 3:** Criação e validação dos 4 Katas em `katas/` com boilerplates em JS e suítes de teste Jest completas.

### **Sprint 2: Execução dos Trials**

* Execução individual das 4 Issues por dev conforme a matriz de Crossover.
* Uso obrigatorio do `timer-cli.js` durante cada *trial*.
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
  --kata kata-01-foo \
  --treatment COM_IA \
  --cmd "npx jest katas/kata-01-foo" \
  --timebox 35

```


3. Durante o trial:
* Pressione **`Shift + T`** para rodar a suíte de testes de aceite.
* O relógio irá parar automaticamente no primeiro evento de sucesso (*Green*) ou ao esgotar os 35 minutos (*Timeout*).