# Fonte dos dados de downloads do npm (T15, #112)

Este é o **2º caminho** do estudo: enquanto o experimento controlado mede desempenho nas 3
máquinas do grupo, aqui medimos **adoção** pela série histórica de downloads dos gerenciadores no
registry público. A proposta descreve o caminho em [proposta.md §3.3](proposta.md).

> **Leia a §4 antes de usar estes números.** Download de pacote **não é** uso do gerenciador, e no
> caso do npm a distância é enorme: ele já vem instalado com o Node.js.

---

## 0. Como reproduzir

```bash
cd "Enunciado 5"
uv run lab05 downloads                    # completa o que falta e regrava os 3 CSVs
uv run lab05 downloads --refresh          # ignora o cache e recoleta a janela inteira
uv run lab05 downloads --until 2026-11-23 # fixa o fim da janela (para refazer a nossa coleta)
```

O comando é **idempotente** e incremental: ele lê `downloads_daily.csv`, descobre o último dia de
cada pacote e só pede à API o que falta. Um pacote já em dia não gera requisição nenhuma, então
rodar duas vezes seguidas não consome o serviço público de graça.

Implementação: [`src/npm_downloads.py`](../src/npm_downloads.py) · testes:
[`tests/test_npm_downloads.py`](../tests/test_npm_downloads.py) (42 casos, nenhum vai à rede).

---

## 1. A fonte

| | |
|---|---|
| Serviço | API pública de downloads do npm |
| Endpoint | `https://api.npmjs.org/downloads/range/<início>:<fim>/<pacote>` |
| Autenticação | nenhuma (API aberta, somente leitura) |
| Pacotes | `npm`, `pnpm`, `bun`, `yarn`, `@yarnpkg/cli` |
| Janela coletada | **2015-01-10 a 2026-11-23** (4.336 dias por pacote, 21.680 linhas) |
| Data da coleta | **24/11/2026** (gravada em `fetched_at`, por pacote) |
| Granularidade | um dia, por pacote |

### 1.1 Limites da API, medidos na prática

Três comportamentos nos morderiam em silêncio se não fossem tratados. Todos estão cobertos por
teste.

| Comportamento | O que acontece | Como o coletor trata |
|---|---|---|
| **Corte silencioso da janela** | Pedir mais de ~550 dias devolve HTTP 200 com uma janela **menor**, sem erro: `2022-01-01:2023-12-31` volta com `start = 2022-06-30`. Quem não confere perde 6 meses sem perceber | A janela é partida em blocos de **500 dias** (`BLOCK_DAYS`) e cada bloco é pedido separadamente |
| **Início dos dados** | Antes de 2015-01-10 a API responde `{"error": "end date > start date"}` | `DATA_START = 2015-01-10` |
| **Limite de requisições** | Depois de ~20 requisições seguidas vem `HTTP 429`, e o cabeçalho `Retry-After` vem **`0`** — obedecer a ele gasta as tentativas em 4 segundos e a coleta morre | 2 s entre requisições (acima do mínimo de 1/s exigido pela T15), e o `Retry-After` só pode **aumentar** a espera: o piso é `BACKOFF_S × tentativa` (30 s, 60 s, 90 s, 120 s) |

Erro da própria API chega com **HTTP 200** e um campo `error` no corpo. O coletor distingue
"pacote sem dados nesta janela" (devolve vazio, normal para datas antes do primeiro release) de
erro de verdade (levanta exceção).

### 1.2 Interrupção não perde trabalho

O CSV diário é regravado **a cada bloco**. Na nossa coleta a API cortou no meio do `bun`, no 24º
bloco; rodar o comando de novo continuou do dia seguinte ao último salvo, sem repetir os 23
blocos já pagos.

---

## 2. Os arquivos

Em [`data/npm_downloads/`](../data/npm_downloads/):

| Arquivo | Uma linha é | Colunas |
|---|---|---|
| `downloads_daily.csv` | um pacote num dia | `package`, `day`, `downloads`, `tool_era` |
| `downloads_weekly.csv` | um pacote numa semana ISO | `package`, `week_start`, `downloads`, `days`, `complete_week`, `tool_era` |
| `downloads_meta.csv` | um pacote | `package`, `label`, `family`, `treatments`, `tool_from`, `first_day`, `last_day`, `days`, `total_downloads`, `tool_era_days`, `tool_era_downloads`, `fetched_at`, `schema_version`, `source_url`, `caveat` |

Observações de uso:

- **`tool_era`** (§3) diz se aquele dia pertence à ferramenta que medimos. **Filtre por
  `tool_era == True`** em qualquer análise de adoção.
- **`complete_week`** marca as semanas de borda, que somam menos de 7 dias. Elas não foram
  apagadas, mas num gráfico de linha enganam: a última semana parece uma queda.
- `treatments` liga o pacote aos ids de `config.MANAGERS`. O `@yarnpkg/cli` aponta para **dois**
  tratamentos (`yarn-berry-nm` e `yarn-berry-pnp`), porque o linker é configuração, não pacote.
- `tool_era` é **recalculado na leitura**, nunca lido do arquivo: corrigir uma data em
  `PACKAGES` conserta os CSVs antigos na próxima execução.

---

## 3. O nome do pacote é mais velho que a ferramenta

Três dos cinco nomes **já existiam** no registry, ocupados por pacotes sem nenhuma relação, e só
foram assumidos anos depois. Os downloads anteriores são de outro software e **não são adoção do
gerenciador**.

| Pacote | Nome criado em | Ferramenta a partir de | Release | Downloads antes disso |
|---|---|---|---|---|
| `npm` | 2013-07-12 | 2013-07-12 | `1.1.25` | — (anterior ao início dos dados) |
| `pnpm` | 2013-03-08 | **2016-02-01** | `0.16.0`, após hiato de 1.059 dias | 334 |
| `yarn` | 2012-03-21 | **2016-10-11** | `0.15.1`, após hiato de 1.624 dias | 2.418 |
| `bun` | 2013-03-13 | **2023-09-08** | `1.0.0` | **45.877.773 (24,1 % do total bruto)** |
| `@yarnpkg/cli` | 2019-09-05 | 2019-09-05 | `2.0.0-rc.4` | — |

O caso do `bun` não é um detalhe: **um quarto de todo o download histórico do nome `bun` é de
outro pacote**, que chegou a passar de mil downloads por dia em 2017 — quatro anos antes de o Bun
existir. Somar a série bruta daria ao Bun um passado que ele não teve.

Datas tiradas do campo `time` de `https://registry.npmjs.org/<pacote>`, no primeiro release depois
do hiato de anos (acesso em 24/11/2026).

**Decisão:** a série bruta é preservada por inteiro — não apagamos dado coletado — e cada dia é
marcado em `tool_era`. Quem analisa filtra; quem audita vê o dado como a API o entregou.

---

## 4. Ameaças de construto

Esta é a seção que limita o que os números podem dizer. Ela detalha a ameaça **Co5** de
[ameacas.md](ameacas.md) e a linha "Downloads ≠ uso" de [proposta.md §10.3](proposta.md).

### 4.1 O npm vem com o Node.js (a mais grave)

Quem instala o Node **recebe o npm junto**. Não há motivo para baixar o pacote `npm` do registry,
e quase ninguém baixa: nos últimos 7 dias da janela o `npm` aparece com **6,2 %** dos downloads
dos cinco pacotes, enquanto o `pnpm` fica com **88,8 %**.

Isso **não** significa que o pnpm seja 14× mais usado que o npm. Significa que a métrica não serve
para comparar o npm com os outros — ela mede *tráfego de instalação do próprio gerenciador*, e o
npm é o único que não precisa desse tráfego. Pelo Stack Overflow Survey (uso declarado, citado na
[proposta.md §2](proposta.md)), o npm continua sendo o mais usado com folga.

**Consequência prática:** a comparação de **níveis** entre o npm e os demais está proibida. O que
se pode ler é a **tendência de cada série ao longo do tempo** e a comparação **entre os
não-npm**, que competem no mesmo canal de distribuição.

### 4.2 Cada ferramenta tem outros canais de instalação

| Gerenciador | Caminhos que **não** passam pelo registry |
|---|---|
| npm | vem com o Node.js |
| pnpm | Corepack, script standalone (`pnpm.io/installation`), Homebrew, Scoop |
| Bun | script oficial (`bun.sh/install`), Homebrew, Docker — o caminho recomendado **não** é o npm |
| Yarn Classic | Corepack, Homebrew, instalador do Windows |
| Yarn Berry | `yarnPath` versionado **dentro do projeto** (é o que fazemos na T03) e Corepack |

Ou seja: todas as séries subestimam o uso, em graus diferentes e desconhecidos. O viés **não é
constante entre os tratamentos**, então a ordem dos downloads não é a ordem da adoção.

O `@yarnpkg/cli` é o caso extremo: 9,6 milhões de downloads em toda a história, contra 1,66 bilhão
do `yarn`. O Berry praticamente não é baixado do registry porque o próprio Berry recomenda fixar o
binário no repositório — exatamente como os nossos lockfiles da T03 fazem.

### 4.3 O pacote `yarn` mistura Classic e Berry

O `yarn` 1.22 é tanto a última versão do Classic quanto o **atalho** que inicia um projeto Berry
(`yarn set version berry`). Um download de `yarn` pode virar uso de Classic ou de Berry. Não há
como separar os dois pela API, então `yarn` → `yarn-classic` é uma atribuição **aproximada**.

### 4.4 Um download não é uma pessoa

A série conta requisições ao registry, e muita coisa que não é adoção entra nela:

- **CI**: um job que roda 50 vezes por dia gera 50 downloads do mesmo pacote para o mesmo projeto;
  um projeto popular pode pesar mais que mil desenvolvedores.
- **Espelhos e proxies** (incluindo Verdaccio, como o nosso) baixam uma vez e servem muitas.
- **Bots, scanners de segurança e reinstalações** contam igual.
- **Imagens Docker** reconstruídas a cada deploy multiplicam o mesmo uso.

Daí os saltos de crescimento da §5 (+404 % no pnpm em um ano) terem de ser lidos como *crescimento
de tráfego*, não como *novos usuários*.

### 4.5 A série é observacional

Não há tratamento atribuído nem controle: a evolução dos downloads convive com lançamentos,
mudanças de CI, campanhas e modas. Qualquer relação entre adoção e desempenho medido (T16, #113) é
**descritiva** — a RQ4 descreve, não explica. Correlação entre 5 pontos não sustenta causalidade,
e nós não a reivindicamos.

---

## 5. O que a coleta mostrou

Última semana da janela (**2026-11-17 a 2026-11-23**) e os dois últimos anos:

| Pacote | 7 dias | Fatia | 365 dias | 365 anteriores | Crescimento |
|---|---:|---:|---:|---:|---:|
| `pnpm` | 357.100.823 | 88,8 % | 6.399.810.217 | 1.269.604.520 | **+404 %** |
| `npm` | 24.878.488 | 6,2 % | 728.653.170 | 381.669.573 | +91 % |
| `yarn` | 13.751.949 | 3,4 % | 468.676.874 | 312.176.945 | +50 % |
| `bun` | 6.419.329 | 1,6 % | 121.381.287 | 15.350.388 | **+691 %** |
| `@yarnpkg/cli` | 123.573 | 0,03 % | 3.886.850 | 2.028.082 | +92 % |
| **Total** | **402.274.162** | 100 % | | | |

Totais históricos na era da ferramenta: `pnpm` 8,64 bi · `npm` 2,37 bi · `yarn` 1,66 bi ·
`bun` 144 mi · `@yarnpkg/cli` 9,6 mi.

Leitura honesta desses números, dadas as ameaças da §4:

- **O que se pode afirmar:** os três desafiantes crescem rápido; o pnpm domina o tráfego de
  instalação por registry e o Bun é o que cresce mais em termos relativos, partindo de uma base
  pequena. O Yarn Classic cresce menos que todos os outros. O Berry pelo registry é marginal.
- **O que não se pode afirmar:** que o pnpm seja mais usado que o npm; que o Berry seja pouco
  usado (ele é pouco *baixado*); que qualquer dessas fatias seja participação de mercado.

---

## 6. Ética

A API é pública, aberta e somente leitura, e a coleta a trata como serviço de terceiro que não nos
deve nada:

- no máximo 1 requisição por segundo — na prática **uma a cada 2 segundos**, e o `--sleep` recusa
  valores abaixo de 1,0 s;
- **cache em CSV**: a janela de 11 anos foi paga **uma vez** (45 requisições); execuções seguintes
  pedem só os dias novos;
- `User-Agent` identificando a coleta como acadêmica e de leitura, **sem nenhum dado pessoal** do
  grupo;
- backoff de 30 s a 120 s quando o serviço pede calma.

Nenhum dado pessoal é coletado: a API devolve apenas contagens agregadas por dia.

---

## 7. De onde vem cada regra

| Regra | Origem |
|---|---|
| API `downloads/range` nos 5 pacotes, janela de vários anos | enunciado da T15 (#112), [PLAN.md](../PLAN.md) |
| ≤ 1 requisição/s, cache em CSV, data da coleta registrada | enunciado da T15 (#112) |
| Documentar que download ≠ uso do npm | enunciado da T15 (#112); detalhado na §4 |
| Blocos de 500 dias, `DATA_START`, backoff com piso próprio | medido contra a API em 24/11/2026 (§1.1) |
| Coluna `tool_era` | achado da coleta: o nome `bun` tem 24 % de downloads de outro pacote (§3) |
| Leitura junto do uso declarado (Stack Overflow Survey) | [proposta.md §2](proposta.md), ameaça **Co5** de [ameacas.md](ameacas.md) |
