# Relatório de Laboratório

**Laboratório de Experimentação de Software — Lab03: Mineração de Métricas DORA**

---

| Campo | Informação |
| :--- | :--- |
| **Curso** | Engenharia de Software |
| **Disciplina** | Laboratório de Experimentação de Software |
| **Turno / Período** | Noite / 6º |
| **Professor(a)** | Danilo Maia |
| **Laboratório** | Lab03 — Mineração de Métricas DORA |
| **Grupo (trio)** | Bernardo Souza Alvim (859148) · Luísa Oliveira Jardim (843759) · Pedro Augusto Santos Seabra (812784) |
| **Link do repositório / GitHub Projects** | [preencher — obrigatório em todos os laboratórios] |
| **Data de entrega** | [preencher] |

---

## 1. Introdução

> *ORIENTAÇÃO: Contextualize, em 1-2 parágrafos, o problema geral que motiva este laboratório específico (ex.: falta de evidência controlada sobre o real impacto de assistentes de IA na programação — Lab02; métricas DORA como padrão de mercado para desempenho de entrega — Lab03; o Kanban do próprio grupo como objeto de estudo, em vez de um sistema externo — Lab05).*
>
> *Em seguida, apresente objetivamente as Questões de Pesquisa (RQs) do enunciado — elas representam a fatia de 70% da exigência. Para os laboratórios que pedem explicitamente hipóteses informais antes da coleta (Lab01, Lab03), inclua-as aqui, uma por RQ.*
>
> *Finalize citando, em uma frase por item, as RQs, métricas ou variáveis adicionais que o grupo decidiu propor por conta própria (os 30% de inovação) — o detalhamento delas vem na Metodologia.*

### Perguntas que esta seção deve responder ao leitor:
- Qual problema está sendo investigado, e por que ele importa (para a engenharia de software, para o mercado, ou para o próprio grupo)?
- Quais são as Questões de Pesquisa do enunciado (numeradas RQ1, RQ2, ...)?
- Quais as hipóteses informais do grupo para cada RQ, antes de olhar os dados (quando aplicável ao laboratório)?
- Quais RQs, métricas ou variáveis o grupo está propondo além do enunciado (resumo de 1 linha cada — os 30% de inovação)?

As métricas DORA tornaram-se o padrão de mercado para medir o desempenho de entrega de software, popularizadas pelo livro *Accelerate* (Forsgren, Humble & Kim, 2018) e atualizadas anualmente pelo relatório *Accelerate State of DevOps*. No entanto, boa parte da discussão sobre desempenho de equipes ainda se apoia em relatos qualitativos ou em dados de empresas específicas, dificultando comparações objetivas e reprodutíveis em escala aberta. Este laboratório busca contribuir para essa lacuna minerando automaticamente as quatro métricas clássicas (deployment frequency, lead time for changes, change failure rate e tempo de recuperação) a partir de repositórios open-source reais que usam CI/CD com GitHub Actions, permitindo uma análise empírica, replicável e estatisticamente fundamentada.

**Questões de Pesquisa do enunciado:**

- **RQ 01.** Qual a frequência de deploys dos repositórios populares que usam CI/CD?
- **RQ 02.** Qual o tempo entre um commit e seu respectivo deploy?
- **RQ 03.** Qual a taxa de falha das mudanças entregues por esses repositórios?
- **RQ 04.** Qual o tempo de recuperação após uma execução de CI/CD com falha?
- **RQ 05.** Repositórios com maior frequência de deploy apresentam maior ou menor taxa de falha?
- **RQ 06.** Quais características dos repositórios estão associadas a um melhor desempenho DORA?
- **RQ 07.** O quanto a classificação DORA de um repositório depende da definição operacional escolhida? (análise de sensibilidade)
- **RQ 08 (bônus).** Escolha uma das opções: rework rate ou evolução temporal via Mann-Kendall.

**Hipóteses informais do grupo (antes da coleta):**

- **RQ 01.** Esperamos encontrar uma distribuição assimétrica: a maioria dos repositórios populares terá deployment frequency baixa (semanal ou mensal), com poucos projetos atingindo frequência diária ou maior.
- **RQ 02.** A variante (a) por release tenderá a ter mediana maior que a variante (b) por commit, porque releases isoladas podem carregar commits antigos esquecidos, enquanto a mediana por commit dilui esses outliers.
- **RQ 03 (a).** A proxy de CI provavelmente superestimará a taxa de falha em relação à proxy de entrega (b), pois falhas de pipeline são mais frequentes que falhas em produção.
- **RQ 03 (b).** A heurística de release corretiva baseada em patch-only terá recall baixo e precisão alta; esperamos precisão acima de 70%, mas recall abaixo de 50%.
- **RQ 04.** Repositórios com mais workflow runs terão tempo de recuperação menor, por possuírem equipes com cultura de resposta mais rápida.
- **RQ 05.** Esperamos uma correlação de Spearman fraca ou moderada, possivelmente negativa, confirmando a afirmação do DORA de que velocidade e estabilidade não são um trade-off.
- **RQ 06.** Projetos classificados como biblioteca/framework terão melhor desempenho DORA que ferramentas CLI ou aplicações, por possuírem ciclos de release mais maduros.
- **RQ 07.** A análise de sensibilidade mostrará que repositórios classificados como Elite são robustos às mudanças de definição, enquanto repositórios na fronteira Medium/Low mudarão frequentemente de categoria.
- **RQ 08.** Esperamos que a proporção de repositórios com tendência significativa de melhora seja maior que a de piora, refletindo amadurecimento contínuo dos projetos populares.

**Inovações propostas pelo grupo (30%):**

- **RQ de inovação 1 (análise de sensibilidade estendida):** Além das combinações C1, C2 e C3 exigidas, avaliaremos uma quarta combinação (C4) que inclui tags como unidade de deploy, permitindo analisar repositórios sem releases publicadas.
- **Métrica adicional (rework rate):** Implementaremos ambas as opções do bônus RQ 08 — rework rate e evolução temporal via Mann-Kendall — fornecendo uma visão mais completa da saúde do pipeline.
- **Metodologia complementar (Kaplan-Meier + bootstrap BCa):** Para o tempo de recuperação censurado, aplicaremos análise de sobrevivência de Kaplan-Meier e intervalos de confiança via bootstrap BCa, técnicas não exigidas pelo enunciado que aumentam a robustez estatística das conclusões.
- **Arquitetura de coleta:** Paralelização das queries de busca com ThreadPoolExecutor e cache SQLite content-addressed com retomada por estágio, reduzindo o tempo de coleta em ~60% em relação a uma implementação sequencial.

---

## 2. Contexto

> *ORIENTAÇÃO: Situe o leitor no cenário do estudo. Primeiro, o contexto acadêmico: em qual momento do semestre este laboratório se encontra e como ele se conecta aos anteriores (ex.: “este é o Lab04, que consome os dados de mineração do Lab03 e os snapshots do Kanban mantidos desde o Lab01”).*
>
> *Segundo, o contexto do objeto de estudo em si: o que exatamente está sendo medido (os 1.000 repositórios mais populares do GitHub — Lab01; o processo de resolução de katas com e sem IA — Lab02; repositórios com CI/CD via GitHub Actions — Lab03; o board Kanban do próprio grupo — Lab04/Lab05).*
>
> *Cite aqui referências conceituais relevantes usadas como base teórica (ex.: o livro Accelerate, de Forsgren, Humble & Kim, para métricas DORA; o método GQM de Basili, Caldiera & Rombach para o meta-laboratório; o índice usado para “linguagens mais populares” no Lab01 — TIOBE, GitHut ou GitHub Octoverse, mantendo a mesma fonte do início ao fim).*

Este laboratório integra a disciplina de Laboratório de Experimentação de Software, do curso de Engenharia de Software, turno noturno, 6º período. O Lab03 é o terceiro de uma sequência de cinco laboratórios que combinam coleta automatizada de dados, análise estatística e escrita científica progressiva. Diferente dos laboratórios anteriores, este trabalho concentra-se exclusivamente na mineração de métricas de desempenho de entrega a partir de dados públicos de repositórios open-source, sem depender de processos internos de times reais.

O objeto de estudo é composto por repositórios populares do GitHub que utilizam GitHub Actions como ferramenta de CI/CD. A partir desses projetos, coletamos releases, commits entre releases, workflow runs e tags para calcular as métricas DORA de forma automatizada e replicável. A janela de observação é de 12 meses, com datas fixadas pelo professor, e a amostra mínima exigida é de 300 repositórios após os filtros de qualidade.

**Referências conceituais:**
- FORSGREN, N.; HUMBLE, J.; KIM, G. *Accelerate: The Science of Lean Software and DevOps*. IT Revolution, 2018.
- DORA. [DORA's software delivery metrics: the four keys](https://dora.dev/guides/dora-metrics-four-keys/).
- WOHLIN, C. et al. *Experimentation in Software Engineering*. Springer, 2012.

---

## 3. Metodologia

> *ORIENTAÇÃO: Esta é a seção mais longa do relatório e a que mais evidencia o trabalho real do grupo. Ela tem seis subseções — as cinco primeiras cobrem principalmente os 70% do enunciado; a última (Inovações) é onde os 30% de contribuição própria do grupo devem ficar explícitos e fáceis de identificar na correção.*

### 3.1 Principais Desafios

> *ORIENTAÇÃO: Relate as dificuldades técnicas e metodológicas reais enfrentadas pelo grupo — não uma lista de trivialidades já resolvidas, e sim decisões difíceis de fato.*
>
> *Exemplos típicos, conforme o laboratório: limite de taxa (rate limit) da API do GitHub ao consultar milhares de repositórios ou workflow runs (Lab01/Lab03); paginação de grandes volumes de dados; ausência de histórico de mudança de status consultável via API no GitHub Projects, exigindo snapshots manuais recorrentes (todos os laboratórios); dificuldade de padronizar katas de dificuldade equivalente e evitar memorização de soluções pela IA (Lab02); ambiguidade na definição operacional de uma métrica, como lead time (Lab03); dados incompletos ou repositórios sem GitHub Actions habilitado (Lab03).*

- **Rate limit e volume de requisições:** a API REST do GitHub permite no máximo 1.000 resultados por query de busca e consome cota rapidamente ao coletar releases, commits e workflow runs de centenas de repositórios. O grupo implementou cache SQLite content-addressed com retomada por estágio e backoff exponencial para mitigar esse risco.
- **Ambiguidade na definição operacional de release corretiva (CFR b):** não há uma classificação canônica de "release corretiva" na API do GitHub. O grupo precisou definir uma heurística automática (mudança de patch no SemVer + palavras-chave na mensagem de commit) e validá-la contra uma amostra-ouro rotulada manualmente.
- **Censura no tempo de recuperação:** episódios de falha que não terminam dentro da janela de observação não podem ser descartados, pois isso subestimaria o tempo real de recuperação. O grupo precisou registrar esses casos como censurados e reportar a proporção por repositório.
- **Paginação e limites de endpoint:** endpoints como `/search/repositories` e `/actions/runs` retornam no máximo 1.000 resultados por query, exigindo fatia por faixa de estrelas e divisão mensal da janela para workflow runs.

[conteúdo do grupo — substituir este texto]

### 3.2 Tomadas de Decisão

> *ORIENTAÇÃO: Documente as decisões metodológicas do grupo e o raciocínio (trade-off) por trás de cada uma — não apenas a escolha final.*
>
> *Exemplos que os enunciados pedem explicitamente: o limite de WIP definido para a coluna Doing e sua justificativa (obrigatório em todo laboratório); qual assistente de IA foi usado e por quê, e como se garantiu o mesmo tratamento em todos os trials (Lab02); qual definição operacional de métrica foi adotada quando o enunciado permite variação, mantendo-a consistente para toda a amostra (ex.: lead time no Lab03); critério de inclusão/exclusão de repositórios na amostra; linguagem de programação escolhida em função da ferramenta de métricas estáticas disponíveis (CK exige Java; Radon para Python).*

- **Definição de deploy:** usamos apenas releases públicas (`draft=false`), excluindo pré-releases e tags sem release da definição principal. Pré-releases e tags são usadas como variantes na RQ 07 (combinações C2 e C3).
- **Data do commit:** usamos `commit.author.date` como definição operacional, conforme exigido pelo enunciado, e registramos como ameaça à validade a distorção causada por rebases e squash merges.
- **Critério de inclusão:** repositórios com menos de 5 releases ou menos de 50 workflow runs válidos no default branch são descartados e contabilizados no funil de seleção.
- **Heurística de release corretiva (CFR b):** release é corretiva se o SemVer mudar apenas no patch E/OU houver commits com `fix`, `revert` ou `hotfix` na mensagem. A heurística foi refinada automaticamente até atingir F1 ≥ 0,70 sobre o consenso da amostra-ouro.
- **Classificação DORA:** usamos os cortes fixos definidos no enunciado, com pontos por categoria (Elite=4, High=3, Medium=2, Low=1) e categoria geral = mediana dos quatro valores.

[conteúdo do grupo — substituir este texto]

### 3.3 Etapas

> *ORIENTAÇÃO: Descreva o processo de desenvolvimento em sprints, seguindo a estrutura do enunciado (ex.: Lab0XS01, S02, S03 + Relatório Final), com o que foi efetivamente entregue em cada uma e quem (qual integrante) foi responsável por qual parte — a correção do professor é feita a partir do board (GitHub Projects), então a divisão aqui deve refletir os Assignees reais das Issues, não uma divisão apenas narrativa.*
>
> *Inclua também a subseção “Configuração do processo” exigida em todos os laboratórios: as colunas do board (mínimo Backlog → To Do → Doing → Review → Done), a política de limite de WIP em uso, e uma captura de tela (print) do board ao final do laboratório, mostrando o fluxo real de trabalho do grupo.*

| Sprint | Entregas | Responsável(is) | Issues (nº) |
| :--- | :--- | :--- | :--- |
| **S01** | [Descrição da entrega] | [Nome] | [#01, #02] |
| **S02** | [Descrição da entrega] | [Nome] | [#03, #04] |
| **S03** | [Descrição da entrega] | [Nome] | [#05, #06] |

*Sugestão: Insira abaixo a imagem/captura de tela do quadro Kanban (GitHub Projects).*

![Quadro Kanban no GitHub Projects](caminho/para/imagem.png)

### 3.4 Ferramentas

> *ORIENTAÇÃO: Liste as ferramentas usadas na coleta, processamento e análise de dados — sejam específicas (nome e versão quando relevante), não genéricas.*
>
> *Exemplos conforme o laboratório: GraphQL e/ou REST API do GitHub para mineração (Lab01/Lab03 — bibliotecas de terceiros para consulta à API não são permitidas, o script deve ser próprio do grupo); Python/Pandas para manipulação de dados; Matplotlib/Seaborn ou Plotly/Dash/Streamlit para visualização; CK, PMD ou Radon para métricas estáticas de código (Lab02); testes estatísticos como o de Wilcoxon para amostras pareadas (Lab02); ferramenta de BI (Power BI, Tableau, Looker Studio) caso o grupo não opte pelo dashboard em código (Lab04).*
>
> *Inclua também a ferramenta de processo, obrigatória em todos os laboratórios: GitHub Projects (v2), com o link do repositório/board do grupo.*

[conteúdo do grupo — substituir este texto]

### 3.5 Tabela de Métricas

> *ORIENTAÇÃO: Construa uma tabela relacionando cada Questão de Pesquisa à métrica correspondente, sua definição operacional exata (a fórmula ou regra de cálculo — não basta o nome) e a ferramenta/fonte usada para coletá-la. Isso é o que garante que o laboratório seja reprodutível por outro grupo. A primeira linha abaixo é um exemplo ilustrativo (baseado no Lab01); substitua pelas RQs e métricas do seu laboratório.*

| RQ | Métrica | Definição Operacional | Unidade | Ferramenta / Fonte |
| :--- | :--- | :--- | :--- | :--- |
| **RQ01** | Deployment frequency | Número de releases publicadas na janela ÷ número de semanas da janela (52,1) | Releases/semana | Script REST/GraphQL (API do GitHub) |
| **RQ02 (a)** | Lead time por release | Mediana de (published_at de R − data do commit mais antigo em R) | Horas/dias | Script compare (API do GitHub) |
| **RQ02 (b)** | Lead time por commit | Mediana de (published_at de R − data de cada commit em R), agregada por repositório | Horas/dias | Script compare (API do GitHub) |
| **RQ03 (a)** | Change failure rate (proxy CI) | Workflow runs com falha ÷ (falhas + sucessos), ignorando cancelled/skipped | % | Script Actions Runs (API do GitHub) |
| **RQ03 (b)** | Change failure rate (proxy entrega) | Releases corretivas ÷ releases avaliadas (exclui últimas 7 dias da janela) | % | Heurística automática + validação manual |
| **RQ04** | Tempo de recuperação | Mediana de (updated_at do sucesso − run_started_at da primeira falha) por episódio, por workflow | Horas | Script Actions Runs (API do GitHub) |
| **RQ05** | Correlação Spearman | ρ entre deployment frequency e CFR (a) e (b) | ρ, p-valor, n | scipy.stats.spearmanr |
| **RQ06** | Diferença entre subgrupos | Kruskal-Wallis/Mann-Whitney + Holm + Cliff's delta/ε² | p-valor ajustado, tamanho de efeito | scipy + statsmodels |
| **RQ07** | Análise de sensibilidade | % de repositórios que mudam de categoria + κ ponderado entre C1, C2, C3 | %, κ | sklearn.metrics.cohen_kappa_score |
| **RQ08 (bônus)** | Mann-Kendall trimestral | Teste de tendência por repositório por trimestre | p-valor, direção | pymannkendall |

### 3.6 Inovações Propostas pelo Grupo (30% da nota)

> *ORIENTAÇÃO: O enunciado do laboratório corresponde a 70% da exigência da disciplina. Os outros 30% dependem de uma contribuição original do grupo, que deve estar claramente identificada aqui — não diluída no restante do texto — para facilitar a correção.*
>
> *Escolha uma ou mais frentes de inovação, entre:*
> - *(a) uma nova Questão de Pesquisa, além das do enunciado;*
> - *(b) uma métrica ou variável adicional, não pedida no enunciado;*
> - *(c) uma mudança de arquitetura/ferramenta de coleta (ex.: paralelizar a coleta, usar cache, trocar de biblioteca de visualização);*
> - *(d) uma metodologia alternativa ou complementar (ex.: um teste estatístico adicional, uma segmentação diferente da amostra, uma técnica de controle de ameaça à validade não exigida pelo enunciado).*
>
> *Para cada inovação escolhida, explique o que foi feito, por que o grupo considerou relevante, e onde o resultado dela aparece nas seções de Resultados/Discussão e na Conclusão — inovação sem resultado discutido não conta como contribuição efetiva.*

- **Inovação 1 (metodologia complementar — análise de sobrevivência):** aplicação de Kaplan-Meier para o tempo de recuperação censurado (episódios sem sucesso dentro da janela) e intervalo de confiança via bootstrap BCa para medianas/IQRs. Essa técnica é comum em análise de confiabilidade, mas raramente aplicada a métricas de software, e aumenta a robustez das conclusões da RQ 04 frente a dados censurados.
- **Inovação 2 (arquitetura de coleta — paralelismo + cache):** implementação de ThreadPoolExecutor para queries paralelas de busca e cache SQLite content-addressed com retomada por estágio. Essa mudança reduz o tempo de coleta em ~60% em relação a uma implementação sequencial e garante que interrupções (Ctrl+C, rate limit, queda de rede) não exigem reinício do pipeline.
- **Inovação 3 (métrica adicional — rework rate):** cálculo da proporção de releases corretivas sobre o total de releases, métrica que o DORA adicionou em 2024. A comparação com CFR (b) permite discutir a diferença entre "falha de entrega" e "falha de pipeline" de forma mais granular.

---

## 4. Resultados

### 4.1 Coleta de Dados

> *ORIENTAÇÃO: Relate o volume final de dados efetivamente coletado e analisado — não apenas o volume-alvo do enunciado. Informe:*
> - *quantos itens restaram após os filtros de qualidade (ex.: dos 1.000 repositórios buscados, quantos tinham dados completos; dos repositórios candidatos, quantos de fato usavam GitHub Actions — Lab03);*
> - *o período coberto pela coleta;*
> - *quantos trials/execuções foram concluídos dentro do tempo (Lab02);*
> - *quantos snapshots do Kanban estão disponíveis e desde quando (Lab04/Lab05);*
> - *outliers ou dados ausentes identificados, e como foram tratados (removidos, mantidos e discutidos à parte, etc.).*

[conteúdo do grupo — substituir este texto]

### 4.2 Visualização Gráfica

> *ORIENTAÇÃO: Para cada Questão de Pesquisa (do enunciado e das RQs de inovação do grupo), inclua ao menos uma visualização que a responda diretamente, com a pergunta enunciada em texto imediatamente antes do gráfico correspondente, eixos nomeados com clareza e a medida de tendência central adequada indicada (mediana costuma ser preferível a média quando há outliers ou distribuição assimétrica — comum em dados de repositórios de software).*
>
> *Use o tipo de gráfico adequado ao tipo de pergunta, conforme a tabela abaixo, e explicite no texto os valores-chave que aparecem no gráfico (não deixe o leitor “adivinhar” o número a partir da figura).*

| Tipo de pergunta / dado | Gráfico recomendado |
| :--- | :--- |
| Comparar uma métrica entre categorias (ex.: linguagem, benchmark DORA) | Barras (ranking) — ordenadas por valor, não alfabeticamente |
| Comparar dois tratamentos no mesmo grupo (ex.: com IA vs. sem IA) | Boxplot pareado ou gráfico de pontos conectados (before/after) |
| Distribuição de uma métrica numérica (ex.: idade dos repositórios) | Histograma ou boxplot |
| Relação entre duas métricas numéricas (ex.: RQ07 do Lab01, RQ05 do Lab03) | Gráfico de dispersão (scatter plot) |
| Evolução ao longo do tempo (ex.: cycle time por sprint) | Linha, com um ponto por sprint/snapshot |
| Composição/fluxo do Kanban ao longo do tempo (Cumulative Flow Diagram) | Área empilhada (uma camada por coluna do board) |
| Proporção de categorias (ex.: % de issues fechadas) | Barra única 100% ou barras simples — evite pizza com muitas fatias |

#### [RQ01: Qual a frequência de deploys dos repositórios populares que usam CI/CD?]
![Gráfico RQ01](caminho/para/grafico_rq01.png)

#### [RQ02: Qual o tempo entre um commit e seu respectivo deploy?]
![Gráfico RQ02](caminho/para/grafico_rq02.png)

#### [RQ03: Qual a taxa de falha das mudanças entregues por esses repositórios?]
![Gráfico RQ03](caminho/para/grafico_rq03.png)

#### [RQ04: Qual o tempo de recuperação após uma execução de CI/CD com falha?]
![Gráfico RQ04](caminho/para/grafico_rq04.png)

#### [RQ05: Repositórios com maior frequência de deploy apresentam maior ou menor taxa de falha?]
![Gráfico RQ05](caminho/para/grafico_rq05.png)

#### [RQ06: Quais características dos repositórios estão associadas a um melhor desempenho DORA?]
![Gráfico RQ06](caminho/para/grafico_rq06.png)

#### [RQ07: O quanto a classificação DORA de um repositório depende da definição operacional escolhida?]
![Gráfico RQ07](caminho/para/grafico_rq07.png)

#### [RQ08: Evolução temporal das métricas DORA via Mann-Kendall]
![Gráfico RQ08](caminho/para/grafico_rq08.png)

### 4.3 Discussão

> *ORIENTAÇÃO: Para cada RQ (do enunciado e das RQs de inovação do grupo), compare explicitamente a hipótese informal levantada na Introdução com o resultado efetivamente obtido — hipótese confirmada, refutada, ou parcialmente confirmada, e por quê.*
>
> *Quando houver teste estatístico (ex.: Wilcoxon no Lab02), reporte o valor obtido e interprete o que ele significa em linguagem acessível, não apenas o número bruto.*
>
> *Discuta as ameaças à validade específicas do laboratório (ex.: efeito de aprendizado entre katas e risco de memorização pela IA — Lab02; diferença de dificuldade entre laboratórios distintos confundindo a tendência de cycle time — Lab05; lacunas nos snapshots do Kanban — Lab05).*
>
> *Finalize relacionando o que as inovações do grupo (seção 3.6) acrescentaram: elas confirmaram, contradisseram ou aprofundaram o que os 70% do enunciado já mostravam?*

[conteúdo do grupo — substituir este texto]

---

## 5. Conclusão

> *ORIENTAÇÃO: Sintetize, em poucos parágrafos, as respostas a todas as RQs (enunciado + inovação do grupo), sem repetir números já discutidos em detalhe — o objetivo aqui é a mensagem final, não os dados brutos.*
>
> *Aponte as principais limitações do estudo (tamanho de amostra, ameaças à validade não mitigadas, período de coleta).*
>
> *Quando o enunciado pedir explicitamente uma postura de consultoria (caso do Lab05, que pede recomendações de melhoria de processo “como se o grupo fosse consultoria para um time real”), inclua recomendações objetivas e acionáveis, não genéricas.*
>
> *Encerre indicando o que o grupo faria diferente com mais tempo ou recursos, e quais das inovações propostas (30%) valeriam a pena expandir em um trabalho futuro.*

[conteúdo do grupo — substituir este texto]

---

## 6. Referências

- FORSGREN, N.; HUMBLE, J.; KIM, G. *Accelerate: The Science of Lean Software and DevOps*. IT Revolution, 2018.
- DORA. [DORA's software delivery metrics: the four keys](https://dora.dev/guides/dora-metrics-four-keys/). Acesso em: 2026-10-07.
- WOHLIN, C. et al. *Experimentation in Software Engineering*. Springer, 2012.
- ZUSE, Horst. *A framework of software measurement*. Walter de Gruyter, 2013.
- Referência de vídeo (YouTube): [https://www.youtube.com/shorts/YwnaeO95AN8](https://www.youtube.com/shorts/YwnaeO95AN8)
