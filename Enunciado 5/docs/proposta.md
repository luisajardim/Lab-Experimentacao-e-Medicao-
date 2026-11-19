# Proposta do estudo — Lab05 (T06, #101)

**Grupo:** Bernardo Alvim, Luísa Jardim, Pedro Seabra · **Disciplina:** Laboratório de
Experimentação de Software · **Sprint:** S01 (19/11/2026)
**Data desta versão:** 16/11/2026 · **Status:** para revisão do trio

> Todos os números de terceiros têm fonte e **data de acesso: 16/11/2026**. As fontes estão
> listadas na seção 13.

---

## 1. Resumo

Comparamos **seis gerenciadores de pacotes do ecossistema Node** instalando **três projetos
reais** em **quatro cenários de instalação**, em **três máquinas Windows 11**, e cruzamos o
desempenho medido com a **adoção real** medida pela API pública de downloads do npm.

| Item | Valor |
|---|---|
| Objeto de estudo | npm (controle), pnpm, Bun, Yarn Classic 1.22, Yarn Berry 4 `node-modules`, Yarn Berry 4 PnP |
| Caminhos | (1) experimento controlado no ambiente do grupo · (2) análise de dados de operação (API de downloads do npm) |
| Desenho | Fatorial 6 × 4 × 3 (gerenciador × cenário × projeto), em blocos (máquina), com ordem aleatorizada e repetições |
| Métrica principal | Tempo de relógio da instalação (`wall_s`) |
| Métricas secundárias | CPU, pico de RAM, pegada em disco (`disk_mb + cache_mb`), nº de arquivos, instalação válida (`build_ok`) |
| Resultado esperado | Quanto cada gerenciador ganha ou perde do npm, com tamanho do efeito e IC, e se as promessas dos fabricantes se confirmam |

O gerenciador de pacotes é um software que **todo projeto Node executa várias vezes por dia**,
em máquina de desenvolvedor e em CI. É software de terceiros, em operação, e o objeto de estudo
é **o programa rodando**, não o repositório dele — o que atende à restrição do enunciado.

---

## 2. O software: real, em operação e de alto impacto

### 2.1 Real

Os seis tratamentos são binários públicos, distribuídos e documentados pelos próprios
fabricantes, não protótipos do grupo:

| Tratamento | Fabricante / projeto | Distribuição |
|---|---|---|
| npm | npm, Inc. / GitHub | vem junto com o Node.js |
| pnpm | pnpm (OpenJS) | pacote `pnpm` no npm |
| Bun | Oven | binário próprio; também publicado como `bun` no npm |
| Yarn Classic 1.22 | Yarn | pacote `yarn` no npm |
| Yarn Berry 4 (`node-modules` e PnP) | Yarn | pacote `@yarnpkg/cli`; release versionado dentro do projeto |

### 2.2 Em operação (versão atual e data do último release)

Consultado em `https://registry.npmjs.org/<pacote>` (campos `dist-tags.latest` e `time`),
**acesso em 16/11/2026**:

| Pacote | Versão mais recente | Publicada em | Versão que usamos |
|---|---|---|---|
| `npm` | 12.2.2 | 04/11/2026 | **11.19.1** (a que acompanha o Node 24 LTS) |
| `pnpm` | 12.21.0 | 13/11/2026 | 12.21.0 |
| `bun` | 1.4.4 | 22/10/2026 | 1.4.4 |
| `@yarnpkg/cli` (Berry) | 4.18.1 | 24/09/2026 | 4.18.1 |
| `yarn` (Classic) | 1.22.22 | **09/03/2024** | 1.22.22 |

Três leituras importantes:

- Cinco dos seis tratamentos tiveram release **nas últimas oito semanas**: são software mantido
  e em uso hoje.
- O **Yarn Classic** não tem release desde março de 2024 (modo de manutenção) e, mesmo assim,
  continua sendo o segundo gerenciador mais usado na pesquisa do Stack Overflow (§2.3). Essa
  distância entre "mantido" e "usado" é parte do que o estudo quer mostrar.
- **Decisão a validar com o trio:** medimos o **npm 11.19.1**, que é o que vem com o Node 24 LTS
  — o que a maioria tem na máquina sem instalar nada. Os benchmarks dos fabricantes comparam
  contra o npm 12 (§6.3). Isso precisa aparecer como ressalva ao testar as promessas.

### 2.3 Alto impacto

**a) Stack Overflow Developer Survey 2025** — 49.009 respostas de 177 países, pesquisa em campo
de 29/05/2025 a 23/06/2025. Na pergunta sobre *cloud platforms, containerization, package
managers, build tools and IaC*:

| Ferramenta | Todos os respondentes | Desenvolvedores profissionais |
|---|---:|---:|
| npm | **56,8 %** (2º no geral, atrás só do Docker) | 59,3 % |
| Yarn | 21,1 % | 23,1 % |
| pnpm | 13,4 % | 14,2 % |
| Bun | 5,5 % | 5,6 % |

Na mesma pesquisa, **Node.js é a tecnologia web mais usada**: 48,7 % de todos os respondentes e
49,1 % dos profissionais. Ou seja: cerca de metade dos desenvolvedores do mundo usa a plataforma
cujo gerenciador de pacotes estamos medindo.

**b) Downloads no registry npm** — API pública `api.npmjs.org/downloads/point/last-week`,
**acesso em 16/11/2026**, semana de 09/11 a 15/11/2026:

| Pacote | Downloads na semana |
|---|---:|
| `pnpm` | 335.515.741 |
| `npm` | 23.755.363 |
| `yarn` | 12.925.307 |
| `corepack` | 8.891.072 |
| `bun` | 5.949.744 |
| `@yarnpkg/cli` | 107.005 |

> **Atenção (ameaça de construto, §10.3):** esses números medem **downloads do pacote**, não uso
> do gerenciador, e os dois não andam juntos. O npm já vem com o Node e quase nunca precisa ser
> baixado; o pnpm costuma ser instalado via `npm i -g pnpm`, inclusive a cada job de CI, o que
> plausivelmente explica boa parte dos 335 milhões; o Bun é instalado principalmente pelo
> instalador próprio, fora do npm; o Yarn Berry é versionado dentro do projeto. Nenhuma dessas
> explicações é verificável pela API — são hipóteses sobre o mecanismo, e é por isso que o número
> sozinho não sustenta conclusão sobre adoção. **Por isso a adoção não é medida só por aqui:** a pesquisa do Stack Overflow (a)
> mede *uso declarado* e produz um ranking quase invertido. Confrontar as duas fontes é um dos
> resultados do caminho 2 (§3.2).

**c) Escala do registry.** Para dimensionar o volume que passa por esses programas, consultamos
os downloads da mesma semana de nove pacotes ubíquos (`semver`, `debug`, `chalk`, `typescript`,
`vite`, `react`, `lodash`, `express`, `next`): **4,22 bilhões de downloads em sete dias**, só
nesses nove. Cada um deles foi servido a um dos gerenciadores que estamos medindo.

**d) State of JS 2025.** A edição 2025 **não tem** uma pergunta geral sobre gerenciadores de
pacotes — conferimos na fonte oficial, e os rankings do tipo "54 % npm / 19 % pnpm" que circulam
em blogs **não estão lá**. O que existe é:

- *Monorepo Tools* ("Which of these monorepo tools do you regularly use?", contagem absoluta de
  respondentes): **pnpm 3.940** (líder), None 3.050, npm Workspaces 2.129, Turborepo 1.718,
  Nx 1.682, Yarn Workspaces 1.341, `bun install` 1.123, Lerna 794.
- *JavaScript Runtimes*: Node.js 10.062, Browser 9.682, **Bun 2.321 (3º)**.
- *Library Tier List*: **Bun com 91 % de satisfaction ratio**, entrando no S-tier.

---

## 3. Pergunta de pesquisa e os dois caminhos

### 3.1 Pergunta

> **Quanto tempo e quanto espaço em disco cada gerenciador de pacotes gasta para instalar
> projetos Node reais no Windows 11, em cada cenário de instalação? As promessas de velocidade
> dos fabricantes se confirmam nesse ambiente? E a adoção real acompanha o desempenho medido?**

Desdobrada em quatro perguntas operacionais, que viram as famílias de hipóteses (§6):

- **RQ1 — Todos × npm.** Cada gerenciador é mais rápido que o npm (o controle), em cada cenário?
- **RQ2 — Yarn × Yarn.** As três variantes do Yarn (Classic, Berry `node-modules`, Berry PnP)
  diferem entre si? Trocar de *linker* vale a pena?
- **RQ3 — Promessa × realidade.** O speedup que medimos bate com o que pnpm e Bun anunciam?
- **RQ4 — Adoção × desempenho.** O gerenciador mais rápido é o mais adotado?

### 3.2 Caminho 1: experimento controlado (no ambiente do grupo)

Rodamos os seis gerenciadores nas nossas máquinas, na mesma versão que roda em produção, e
**manipulamos o tratamento** (qual gerenciador) mantendo tudo o mais fixo. É o caminho "Rodar o
software no ambiente do grupo" do enunciado.

### 3.3 Caminho 2: dados de operação (API de downloads do npm)

Coletamos a **série histórica de downloads** de `npm`, `pnpm`, `yarn`, `@yarnpkg/cli` e `bun` na
API pública do registry (`api.npmjs.org/downloads/range`), com no máximo 1 requisição por
segundo e cache em CSV (T15, #112). É o caminho "Analisar dados de operação".

### 3.4 Por que combinar os dois

O enunciado valoriza estudos que combinam caminhos, e aqui a combinação não é decorativa — cada
caminho responde o que o outro não consegue:

- O **experimento** mede causalidade com controle, mas numa amostra minúscula do mundo (3
  máquinas, 3 projetos, só Windows). Ele diz *qual é mais rápido aqui*, não *o que o mercado faz*.
- Os **dados de operação** cobrem o mundo inteiro e vários anos, mas são observacionais: não
  controlam nada e medem download, não uso.
- Juntos respondem à RQ4, que é a pergunta mais interessante do estudo: **se o desempenho
  explicasse a adoção, o ranking de velocidade e o de uso seriam parecidos.** Os dados de §2.3 já
  sugerem que não são — o npm, nosso controle e provavelmente o mais lento, é o mais usado por
  ampla margem. O experimento quantifica *quanto* se perde com essa escolha.

---

## 4. GQM (template de Basili)

### 4.1 Objetivo

> **Analisar** os gerenciadores de pacotes do ecossistema Node (npm, pnpm, Bun, Yarn Classic,
> Yarn Berry `node-modules` e Yarn Berry PnP)
> **com o propósito de** caracterizar e comparar
> **com respeito a** tempo de instalação, consumo de CPU e memória, pegada em disco e validade da
> instalação
> **do ponto de vista de** quem desenvolve e de quem mantém pipelines de CI
> **no contexto de** três projetos Node gerados pelos templates oficiais (API Express, React +
> Vite e Next.js), em quatro cenários de instalação, em três máquinas Windows 11 do grupo, com um
> registry npm local (Verdaccio) isolando a rede.

### 4.2 Perguntas e métricas

| Pergunta (Q) | Métricas (M) | Escala |
|---|---|---|
| **Q1.** Quanto tempo cada gerenciador leva para instalar, em cada cenário? | `wall_s` (mediana e IQR por célula) | razão |
| **Q2.** Qual o ganho (ou perda) em relação ao npm? | speedup = mediana(npm) / mediana(M); Cliff's δ | razão / ordinal |
| **Q3.** Quanto custa em CPU e memória? | `cpu_s`, `peak_rss_mb` | razão |
| **Q4.** Quanto ocupa em disco? | `disk_mb + cache_mb` (pegada total), `n_files` | razão |
| **Q5.** A instalação funciona de fato? | `build_ok` (proporção), `exit_code` | nominal |
| **Q6.** O cenário muda o ranking? | `wall_s` por cenário (`cold`, `ci`, `warm-cache`, `reinstall`) | razão × nominal |
| **Q7.** A adoção acompanha o desempenho? | downloads semanais (série da API) × speedup medido | razão |

**Entidades e atributos.** A entidade medida é o **processo** de instalação — um *recurso* (o
gerenciador) agindo sobre um *produto* (o projeto). `wall_s`, `cpu_s`, `peak_rss_mb`, `n_files`,
`disk_mb` e `cache_mb` são **medidas diretas** de **atributos externos** (dependem do ambiente:
máquina, disco, antivírus). `speedup`, `pegada total` e `taxa de build_ok` são **derivadas**.

---

## 5. Desenho do experimento

### 5.1 Variáveis

| Papel | Variável | Valores |
|---|---|---|
| **Independente (tratamento)** | gerenciador | 6: npm (**controle**), pnpm, bun, yarn-classic, yarn-berry-nm, yarn-berry-pnp |
| **Independente (fator)** | cenário | 4: `cold`, `ci`, `warm-cache`, `reinstall` |
| **Independente (fator)** | projeto-carga | 3: `express-api`, `react-vite`, `next-app` |
| **De bloco** | máquina | 3 (uma por integrante), com specs registradas |
| **Dependentes** | `wall_s` (principal), `cpu_s`, `peak_rss_mb`, `disk_mb`, `cache_mb`, `n_files`, `build_ok` | — |
| **Fixas (controladas)** | Node 24.22.3; versões exatas dos 6 gerenciadores; registry local; mesmo `package.json` nos 6 tratamentos; Defender no padrão; perfil de energia "alto desempenho"; Windows Update pausado; máquina na tomada | — |
| **Aleatorizada** | ordem de execução das células, por bloco e repetição (semente fixa) | — |

São **72 células** (6 × 4 × 3) por máquina. Com N repetições, 72 × N instalações medidas por
bloco; a estimativa inicial é N = 10 (≈ 720 por máquina), mas **o N definitivo sai da análise de
poder** sobre a variância do piloto (§7.3).

### 5.2 Cenários (o que existe *antes* da instalação medida)

Seguem o esquema da própria página de benchmarks do pnpm, o que torna a comparação com as
promessas dos fabricantes direta (§6.3):

| Cenário | Lockfile | Cache | `node_modules` | Situação real que representa |
|---|---|---|---|---|
| `cold` | não | não | não | primeira instalação do projeto, máquina nova |
| `ci` | sim | não | não | pipeline de CI sem cache (o caso mais comum) |
| `warm-cache` | sim | sim | não | CI com cache restaurado |
| `reinstall` | sim | sim | sim | `install` repetido com tudo no lugar |

### 5.3 Objetos (projetos-carga)

Três projetos gerados pelos **templates oficiais**, com versões exatas, já prontos e validados
(T03, #98 — ver [`../projects/README.md`](../projects/README.md)):

| Projeto | Origem | Diretas | Transitivas | Perfil |
|---|---|---:|---:|---|
| `express-api` | escrito à mão (não há template oficial de servidor Express) | 4 | 82 | muitos pacotes pequenos |
| `react-vite` | `create-vite` 9.3.4, template `react-ts` | 9 | 88 | poucos pacotes grandes |
| `next-app` | `create-next-app` 16.4.6, App Router + TS | 7 | 53 | poucos pacotes muito grandes |

Não usamos repositório de terceiros como carga, conforme o enunciado: **o objeto de pesquisa é o
gerenciador em funcionamento**, e o projeto é só a carga que ele processa.

### 5.4 Instrumentação

- **Runner** (`src/runner.py`, T04 #99): monta um diretório limpo, prepara o cenário, mede a
  instalação, mede o disco, roda o `build` e grava uma linha em `runs.csv`. Detalhes em
  [`runner.md`](runner.md); o formato dos dados, em [`schema.md`](schema.md).
- **Registry local (Verdaccio 7.1.0)**, T02 #97: todos os tratamentos instalam de
  `http://localhost:4873/`. Sem isso, o tempo medido misturaria o gerenciador com a internet de
  cada casa — e faríamos centenas de downloads no registry público (§11, ética).
- **Ambiente padronizado:** `scripts/windows_portable.ps1` baixa as versões fixadas numa pasta só,
  sem instalar nada no sistema. O `collect` **aborta** se alguma versão estiver fora do esperado.
- **Aleatorização e aquecimento:** a ordem das células é uma permutação por repetição, com semente
  derivada do nome da máquina; as rodadas de aquecimento ficam gravadas com `warmup = true` e são
  descartadas na análise.

### 5.5 Três decisões de método que mudam o construto

Precisam estar na proposta porque **mudam o que estamos medindo**, não só como medimos:

1. **O npm roda com `--no-audit --no-fund`.** O `audit` faz uma requisição extra ao registry (que
   o Verdaccio nem sempre atende) e **nenhum outro gerenciador audita na instalação**. Medir o
   npm com audit ligado compararia coisas diferentes. É também a configuração típica de CI.
   *Consequência honesta:* o que medimos é "npm como se usa em CI", não "npm como vem de fábrica"
   — e a auditoria é um recurso de segurança que o npm oferece e os outros não. Isso vai para as
   ameaças de construto e para a discussão de impacto.
2. **Pegada em disco = `disk_mb + cache_mb`.** O pnpm (e o Yarn com cache global) liga o store ao
   `node_modules` por hard link: o mesmo byte aparece nos dois lugares. O runner conta cada inode
   uma vez, põe no projeto o que está ligado e deixa em `cache_mb` só o que é exclusivo do cache.
   Comparar só `disk_mb` ou só `cache_mb` entre gerenciadores dá resultado errado.
3. **Política de idade de versão desligada no pnpm e no Yarn Berry.** Esses dois recusam, por
   padrão, pacotes publicados há menos de 24 h (`minimumReleaseAge` e `npmMinimalAgeGate`); npm,
   Bun e Yarn Classic não têm nada parecido. Com a política ligada, esses dois **falhariam** em
   instalações que os outros quatro concluem, e a diferença medida deixaria de ser desempenho.
   Desligamos nos dois e registramos a decisão (ver `projects/README.md`).

---

## 6. Hipóteses

Todas **bicaudais**, com **α = 0,05**, sobre a **mediana** (as distribuições de tempo são
assimétricas, com cauda à direita). O teste roda **por cenário**, porque o ranking pode mudar de
um cenário para outro — e isso é exatamente a Q6.

### 6.1 RQ1 — Todos × npm (controle)

Para cada gerenciador M ∈ {pnpm, bun, yarn-classic, yarn-berry-nm, yarn-berry-pnp} e cada
cenário c:

- **H₀:** mediana(`wall_s` | M, c) = mediana(`wall_s` | npm, c)
- **H₁:** mediana(`wall_s` | M, c) ≠ mediana(`wall_s` | npm, c)

São **5 comparações contra o controle** por cenário (não 15 pares), o que reduz a penalidade da
correção múltipla. Teste: **Wilcoxon pareado** (pares por máquina × projeto × repetição), com
correção de **Holm** dentro de cada cenário.

A mesma estrutura se repete para a **pegada em disco** (`disk_mb + cache_mb`).

### 6.2 RQ2 — Yarn × Yarn

Para cada cenário c, entre Classic, Berry `node-modules` e Berry PnP:

- **H₀:** as três variantes têm a mesma mediana de `wall_s`
- **H₁:** pelo menos uma difere

Teste: **Friedman** (três medidas pareadas) e, se rejeitar, **post-hoc Wilcoxon com Holm**. É a
comparação mais limpa do estudo: mesmo fabricante, mesmo binário de entrada, mudando só a versão
e o *linker*.

### 6.3 RQ3 — Promessas dos fabricantes

Os dois fabricantes publicam números. Traduzidos para os nossos cenários (acesso em 16/11/2026):

| Nosso cenário | Cenário do fabricante | pnpm × npm (anunciado) | Bun × npm (anunciado) |
|---|---|---:|---:|
| `cold` | "clean" / "first install, ever" | 7,6× – 9,7× | ≈ 12,9× |
| `ci` | "lockfile" / "CI without a cache" | ≈ 3,2× | ≈ 5,2× |
| `warm-cache` | "cache + lockfile" / "CI with warm cache" | 6,4× – 7,2× | ≈ 21,2× |
| `reinstall` | "everything warm" / "everything already up to date" | **42× – 120×** | ≈ 28× |

Os valores são a razão entre os tempos publicados em `pnpm.io/benchmarks` (dados coletados em
13/11/2026; faixa = os projetos *alotta-files* e *alotta-packages*) e em `bun.com/package-manager`
(Linux x64, EPYC 9R14, medianas de 3). O Bun ainda anuncia, na documentação, "**up to 25x
faster**" que o `npm install`, sem dizer em qual cenário.

Para cada par (gerenciador, cenário):

- **H₀:** o speedup anunciado está dentro do IC 95 % do speedup que medimos
- **H₁:** está fora

Operacionalmente: calculamos o speedup observado (razão das medianas) com **IC 95 % por
bootstrap** e verificamos se o valor anunciado cai dentro. **Quatro ressalvas que já conhecemos**
e que serão declaradas junto do resultado:

- Os fabricantes medem em **Linux**; nós medimos em **Windows 11**, onde criar muitos arquivos
  custa notoriamente mais caro. Uma divergência não significa que o fabricante mentiu.
- Eles comparam contra o **npm 12**; nós usamos o **npm 11.19.1** do Node 24 LTS (§2.2).
- Os projetos são outros, e o benchmark do pnpm **não inclui Bun nem Yarn**: não existe
  comparação direta publicada pelos próprios autores entre os dois concorrentes.
- Na página do Bun, a mesma medição aparece como `0.21s` no gráfico e `210 s` na tabela
  (provavelmente milissegundos). Usamos a leitura do gráfico e registramos a inconsistência.

### 6.4 RQ4 — Adoção × desempenho

**Descritiva, sem teste de hipótese.** São apenas cinco gerenciadores: qualquer correlação com
n = 5 teria poder desprezível e seria um exercício de ruído. Reportamos a série de downloads, a
participação de cada um, o crescimento no último ano e um gráfico adoção × speedup, com as
limitações explícitas (§10.3).

### 6.5 Compatibilidade (resultado à parte)

`build_ok` **não é hipótese de desempenho**: é um resultado de compatibilidade, reportado como
proporção por gerenciador e projeto. Já temos um achado da T03: o Yarn PnP não constrói os dois
front-ends com a configuração padrão dos templates (o `tsc` não resolve `types` sem
`node_modules/@types`; o Turbopack do Next 16 não enxerga o PnP). Isso é resultado, não defeito do
experimento.

---

## 7. Plano de análise

> Alinhado com o Pedro (T08 #103, T09 #104). **Pendente de confirmação dele** antes de fechar a S01.

### 7.1 Descritiva

Mediana e IQR de `wall_s` por célula; boxplot por gerenciador × cenário, com cor fixa por
gerenciador (`config.PALETTE`); tabela de pegada total; taxa de `build_ok`. Checagem de efeito de
ordem usando a coluna `order`.

### 7.2 Testes

| Comparação | Teste | Correção |
|---|---|---|
| Todos × npm (por cenário) | Wilcoxon pareado | Holm (5 comparações) |
| Yarn × Yarn (por cenário) | Friedman → post-hoc Wilcoxon | Holm |
| Promessa × medido | IC 95 % por bootstrap do speedup | — |

Os testes são **não paramétricos** por decisão de escala e de forma: o tempo é de razão, mas as
distribuições são assimétricas e sujeitas a outliers de ambiente (antivírus, serviço do Windows
acordando no meio da medição). A validação de `src/stats.py` é feita contra `scipy.stats`.

### 7.3 Tamanho do efeito e poder

- **Tamanho do efeito:** **Cliff's δ** (não paramétrico, sem suposição de forma) e **speedup**
  (razão das medianas), ambos com IC 95 % por bootstrap.
- **Poder:** simulação no estilo do `sample_size.py` do Lab04 — reamostra os tempos do **piloto**
  (T05, #100), aplica efeitos de 10 %, 20 % e 30 % e estima o poder do Wilcoxon com Holm. O **N de
  repetições sai daí** (T09), cruzado com o tempo total de coleta: se não couber até 23/11, o
  corte proposto é o cenário `reinstall` ou um projeto — nunca reduzir N.

---

## 8. As 7 categorias da pesquisa

| # | Categoria | Classificação | Justificativa |
|---|---|---|---|
| 1 | **Natureza** | **Aplicada** | Não buscamos uma lei geral: queremos subsidiar uma decisão concreta e cotidiana ("qual gerenciador adotar neste projeto, neste sistema operacional"). O produto é uma recomendação com números, não teoria. |
| 2 | **Objetivos** | **Explicativa** (com parte descritiva) | O caminho 1 manipula a causa (o gerenciador) e observa o efeito (tempo, disco), estabelecendo relação causal dentro do ambiente controlado. O caminho 2 é descritivo: caracteriza a adoção ao longo do tempo, sem explicar por quê. |
| 3 | **Abordagem** | **Quantitativa** | Todas as variáveis de resposta são numéricas e medidas por instrumentação automática; a análise é estatística. Não há coleta de percepção, entrevista ou codificação qualitativa. |
| 4 | **Procedimentos** | **Experimental** (caminho 1) + **documental / ex-post-facto** (caminho 2) | Caminho 1: tratamento manipulado, objetos submetidos a todos os tratamentos, ordem aleatorizada, repetição e blocos — experimento em sentido estrito. Caminho 2: usa dados já produzidos pela operação do registry, sobre os quais não temos controle nenhum. |
| 5 | **Tempo** | **Transversal** (caminho 1) + **longitudinal** (caminho 2) | O experimento é um retrato de novembro/2026, com versões congeladas. A série de downloads cobre vários anos e é analisada como evolução. |
| 6 | **Controle** | **Alto no caminho 1, nulo no caminho 2** | Caminho 1: controlamos versão, rede (registry local), máquina (bloco), carga, cenário, ordem e energia; o único fator deliberadamente livre é o tratamento. Caminho 2: observacional puro — nenhuma variável é manipulada e há confundidores óbvios (CI, bots, mirrors). |
| 7 | **Nível de evidência** | **Alto no caminho 1 dentro do escopo; baixo no caminho 2** | O caminho 1 é um experimento controlado, aleatorizado, repetido e em blocos: dentro do escopo (3 máquinas Windows 11, 3 projetos, registry local), a evidência é forte. **Fora dele, não generaliza**: não fala de Linux, macOS, monorepos grandes ou rede real. O caminho 2 é correlacional e com construto frágil (download ≠ uso), então sustenta descrição, nunca causa. |

**Um experimento sem sujeitos humanos.** Os "sujeitos" aqui são **objetos** (projetos e
máquinas), não pessoas. Isso elimina ameaças clássicas (aprendizado, maturação, mortalidade
experimental, efeito do experimentador sobre participantes) e dispensa consentimento, mas
introduz outras: estado da máquina, antivírus e cache do sistema de arquivos (§10).

---

## 9. Conceitos da disciplina teórica aplicados

### 9.1 Medição e armadilhas

- **Lei de Goodhart** — "quando uma medida vira meta, deixa de ser uma boa medida". O "tempo de
  instalação" é **exatamente** a métrica que os fabricantes otimizam e anunciam, então é a mais
  suscetível a ser jogada. Dois exemplos concretos dentro do nosso desenho: o **Yarn PnP não cria
  `node_modules`** (fica rapidíssimo, mas muda a semântica da instalação) e o **Bun não roda
  scripts de pós-instalação por padrão** (pula trabalho que o npm faz). *Mitigação:* medimos
  `build_ok` (a instalação serve?), `n_files` e a pegada total, não só o relógio.
- **Lei de Campbell** — quanto mais uma métrica é usada para decidir, mais ela distorce o processo
  que mede. Aplicada aqui: escolher gerenciador só pelo benchmark do fabricante é decidir por um
  número produzido por quem tem interesse no resultado. Daí a RQ3.
- **Falácia de McNamara** — tratar como irrelevante o que não foi medido. Este estudo **não mede**
  segurança (o `audit` que desligamos), experiência de uso, qualidade do suporte a monorepos nem
  estabilidade em projetos grandes. A conclusão precisa dizer isso com todas as letras.

### 9.2 Escalas e estatísticas permitidas

| Escala | Variáveis | O que é permitido |
|---|---|---|
| Razão | `wall_s`, `cpu_s`, `peak_rss_mb`, `disk_mb`, `cache_mb`, `n_files` | tudo; usamos mediana/IQR e razões (speedup) por causa da assimetria |
| Nominal | `manager`, `scenario`, `project`, `registry`, `build_ok` | contagens e proporções |
| Ordinal | `rep`, `order` | ordenação; `order` serve para checar efeito de ordem |
| Intervalar | `timestamp` | diferenças, não razões |

Como o tempo está numa escala de **razão**, o speedup (uma razão) é uma estatística legítima — o
que não seria verdade numa escala intervalar.

---

## 10. Ameaças à validade (primeira versão)

> Versão completa, com mitigações detalhadas, na T17 (#114). Aqui ficam as que já orientam
> decisões de desenho.

### 10.1 Conclusão

| Ameaça | Mitigação |
|---|---|
| Variância do ambiente (antivírus, serviços, térmico) inflando o erro | Protocolo fixo (T07), aquecimento descartado, repetições, mediana e testes não paramétricos |
| N insuficiente → não detectar efeito real | Análise de poder sobre o piloto define o N (T09) |
| Múltiplas comparações → falso positivo | Correção de Holm; comparações contra o controle (5), não todos os pares (15) |
| Supor normalidade numa distribuição assimétrica | Wilcoxon/Friedman e bootstrap, sem suposição de forma |

### 10.2 Interna

| Ameaça | Mitigação |
|---|---|
| Efeito de ordem e aquecimento do sistema de arquivos | Ordem aleatorizada por repetição com semente fixa; rodadas de aquecimento marcadas e descartadas |
| Cache residual de uma medição contaminando a seguinte | O cache de cada gerenciador é apagado e reconstruído a cada instalação |
| Versões diferentes entre máquinas | Ambiente portátil com versões fixadas; `collect` aborta se alguma divergir |
| `yarn-classic` virar Berry sem aviso (o Yarn 1.22 obedece a `.yarnrc.yml` de pastas acima) | Checagem de versão antes da coleta; proibição de `.yarnrc.yml` acima do projeto |
| Gerenciador ignorar em silêncio a configuração de cache ou de registry (o pnpm 12 ignorou `npm_config_*` no piloto) | Antes de coletar, o runner pergunta a cada gerenciador onde fica o cache e qual é o registry, e aborta se divergir; as linhas afetadas do piloto foram recoletadas |
| Windows Update ou Defender agindo no meio da coleta | Update pausado; Defender **fixo no padrão** (vira limitação declarada, não fator) |

### 10.3 Construto

| Ameaça | Mitigação / declaração |
|---|---|
| "Tempo de instalação" ≠ produtividade do desenvolvedor | Declarada; o impacto (T20) traduz tempo em horas de CI, não em produtividade |
| **Downloads ≠ uso** do gerenciador | Declarada e **central**: o npm vem com o Node, o pnpm é reinstalado a cada job de CI, o Bun tem instalador próprio. Por isso a adoção é lida junto com o Stack Overflow Survey, que mede uso declarado |
| `build_ok` como proxy de "instalação válida" | É um proxy forte (o projeto compila), mas não cobre runtime nem testes |
| npm com `--no-audit --no-fund` ≠ npm de fábrica | Declarada (§5.5); o audit é um recurso que só o npm oferece |
| Disco com hard links contado em dobro | `disk_mb + cache_mb`, com dedup por inode |
| Políticas de idade desligadas no pnpm e no Berry | Declarada (§5.5): sem isso, mediríamos política de segurança, não desempenho |

### 10.4 Externa

| Ameaça | Mitigação / limite declarado |
|---|---|
| Só Windows 11, só três máquinas, todas de estudantes | Specs registradas por bloco; o resultado é declarado como válido para esse perfil |
| Registry local (Verdaccio) ≠ internet real | Rodada de checagem contra o registry público (T19, #116) |
| Três projetos pequenos ≠ monorepo de empresa | Declarada; os três cobrem perfis diferentes (muitos pacotes pequenos × poucos grandes), mas nenhum é grande |
| Versões congeladas em nov/2026 | Versões exatas publicadas; o estudo é um retrato datado |

---

## 11. Ética

- **Nenhum teste de carga em sistema de terceiros.** O experimento roda contra um **registry
  local**. A API de downloads do npm é consultada **somente para leitura**, com no máximo **1
  requisição por segundo** e cache em CSV.
- **O Verdaccio baixa cada pacote do registry público uma única vez** e serve as centenas de
  instalações seguintes a partir do cache local. Sem isso, a coleta completa faria milhares de
  downloads desnecessários num serviço público e gratuito.
- **Nenhum dado pessoal** é coletado. Não há participantes humanos, logo não há consentimento a
  obter. As specs gravadas são de hardware, não de pessoa.

---

## 12. O que reaproveitamos dos laboratórios anteriores

| Lab | O que volta | Onde |
|---|---|---|
| **Lab01** | Coleta automatizada via API pública e Kanban no GitHub Projects | Caminho 2 (T15) e o próprio quadro de issues |
| **Lab02** | Desenho com tratamentos, aleatorização e repetição | §5 |
| **Lab03** | Métricas DORA: a instalação é parte do **lead time** do pipeline de CI | Tradução do impacto (T20) |
| **Lab04** | Escolha do teste, simulação de poder, bootstrap, dashboard Streamlit e deploy | §7 e o dashboard (T10, T11) |

**Novo neste lab:** registry local para isolar a rede, medição de CPU/RAM/disco com dedup por
inode, e a comparação entre a promessa do fabricante e a medição independente.

---

## 13. Fontes

Todas acessadas em **16/11/2026**.

| # | Fonte | URL | O que tiramos |
|---|---|---|---|
| 1 | Stack Overflow Developer Survey 2025 — Technology | https://survey.stackoverflow.co/2025/technology | npm 56,8 % / Yarn 21,1 % / pnpm 13,4 % / Bun 5,5 %; Node.js 48,7 % |
| 2 | Stack Overflow Developer Survey 2025 — Methodology | https://survey.stackoverflow.co/2025/methodology/ | 49.009 respostas, 177 países, campo de 29/05 a 23/06/2025 |
| 3 | State of JavaScript 2025 — Other Tools | https://2025.stateofjs.com/en-US/other-tools/ | Monorepo tools (pnpm 3.940, líder); runtimes (Bun 3º, 2.321) |
| 4 | State of JavaScript 2025 — Libraries | https://2025.stateofjs.com/en-US/libraries/ | Bun com 91 % de satisfaction ratio (S-tier) |
| 5 | npm registry — metadados dos pacotes | https://registry.npmjs.org/ | versão mais recente e data de publicação de cada gerenciador |
| 6 | npm — API pública de downloads | https://api.npmjs.org/downloads/point/last-week/ | downloads semanais dos gerenciadores e dos 9 pacotes ubíquos |
| 7 | pnpm — Benchmarks | https://pnpm.io/benchmarks | tempos anunciados por cenário (dados coletados em 13/11/2026) |
| 8 | Bun — Package manager | https://bun.com/package-manager | tempos por cenário (Linux x64 EPYC 9R14, medianas de 3) |
| 9 | Bun — `bun install` (docs) | https://bun.com/docs/cli/install | "up to 25x faster" que o `npm install` |

Documentos internos: [`schema.md`](schema.md) (formato dos dados), [`runner.md`](runner.md)
(instrumentação), [`registry.md`](registry.md) (registry local),
[`../projects/README.md`](../projects/README.md) (projetos-carga) e [`../PLAN.md`](../PLAN.md)
(plano das sprints).

---

## 14. Pendências da S01 (situação em 19/11)

1. **Revisão do trio** (critério de aceitação desta tarefa): em aberto até a entrega.
2. **Pedro, §7 e N:** resolvido. Testes implementados em `src/stats.py` (T08) e
   **N = 10 repetições por máquina** pela análise de poder sobre o piloto (T09, `docs/poder.md`).
3. **Bernardo, §5.5 item 1 e piloto:** resolvido. O runner roda o npm com `--no-audit --no-fund`
   em todos os cenários (`src/runner.py`). O piloto (T05, 17/11, 182 instalações, nenhuma falha de
   instalação nem de build) revelou um problema de instrumentação: o pnpm 12 ignorava em silêncio as
   variáveis `npm_config_*`, então usou um store fora do cache isolado e o registry público. As 30
   linhas do pnpm foram descartadas e recoletadas depois da correção, e a coleta agora aborta se
   algum gerenciador não usar o cache e o registry esperados (§10.2).
4. **npm 11.19.1 × 12.2.2:** adotado o **11.19.1** (o que vem com o Node 24 LTS), que é a versão
   fixada no ambiente portátil e usada no piloto. A ressalva entra na RQ3.
