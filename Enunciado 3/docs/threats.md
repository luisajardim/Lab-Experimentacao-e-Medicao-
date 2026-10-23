# Ameaças à validade

Classificação de Wohlin et al. (2012, *Experimentation in Software Engineering*, cap. 8):
**construto**, **interna**, **externa** e **conclusão**. Cada ameaça cita a evidência do
próprio estudo que a sustenta e o que foi feito para mitigá-la. Os números vêm dos artefatos
versionados em `analysis/output/`, `reports/` e `data/gold/`.

> Resumo: a classificação DORA mostrou-se **razoavelmente robusta** à definição operacional
> (RQ07, κ linear 0,67–0,84), mas a validade de construto da CFR(b)/rework rate e a
> **independência da amostra-ouro** são os pontos mais frágeis do estudo (ver C3 e C4).

---

## 1. Validade de construto — estamos medindo o que achamos que medimos?

| # | Ameaça | Evidência no estudo | Mitigação / impacto |
|---|---|---|---|
| C1 | **Release ≠ deploy.** Uma release publicada no GitHub não garante entrega em produção (bibliotecas publicam em registries; apps podem ter deploy contínuo sem release). | Na RQ07, incluir tags com data como deploy (C1→C2) mudou a categoria de **14,6%** dos repositórios, todos para uma categoria **melhor** (36 melhoraram, 0 pioraram). | A unidade de deploy é parte da definição testada na RQ07; o efeito é reportado e tem direção conhecida (C1 é conservadora). |
| C2 | **CFR (a) é um proxy de CI, não de falha em produção.** Workflow com `failure` mede quebra de build/teste, não incidente no usuário. | Mediana CFR(a) = **5,3%** contra mediana de rework rate = **87,5%** (RQ08): os dois proxies medem fenômenos distintos. Spearman DF×CFR(a) ρ = **0,13**; DF×CFR(b) ρ = **0,64** (RQ05). | As duas variantes são reportadas lado a lado; as conclusões da RQ05 são separadas por variante. |
| C3 | **Heurística de release corretiva superestima correções.** A heurística escolhida (`v2`, palavras `fix/revert/hotfix` como palavra inteira ou bump de PATCH) tem **precisão 0,73 e recall 1,00** contra o consenso (F1 = 0,84; CV 5×20: 0,80–0,84). | ~27% das releases marcadas como corretivas não o são segundo os avaliadores. Isso infla CFR(b) e a rework rate (RQ08). Além disso, CFR(b) e deployment frequency compartilham a mesma base (contagem de releases), o que **acopla** os construtos e pode explicar parte do ρ = 0,64 da RQ05. | Histórico das versões testadas em `docs/cfr_heuristic_history.md`; meta F1 ≥ 0,70 atingida. Os valores absolutos de CFR(b)/rework devem ser lidos como **limite superior**. |
| C4 | **Independência e origem humana dos rótulos da amostra-ouro.** O protocolo (ENUNCIADO §6) pede três avaliadores humanos independentes. | Na rodada original de rotulagem (commit `64c1242`), o κ de Fleiss foi **0,615** (tipo, substancial), **0,068** (entrega, leve) e **0,552** (corretiva, moderada). Nessa rodada, o avaliador B foi declarado como LLM (Claude) em `labels_B.audit.json`, e os avaliadores A e C usaram **pré-rotulagem por LLM** (`scripts/llm_prelabel.py`) com revisão humana. Após a nova amostra-ouro do commit `ef9a837` (#74), `labels_A/B/C.csv` ficaram **idênticos campo a campo**, e `reports/agreement.md` passou a reportar κ = **1,000** em todas as dimensões. | **Pendente (grupo):** o κ = 1,000 atual não mede concordância independente e não deve ser usado no artigo. Reportar o κ da rodada original ou refazer a rotulagem B/C na nova amostra. O uso de LLM deve ser declarado na metodologia. |
| C5 | **Data do commit (`commit.author.date`).** Rebase e squash merge reescrevem ou agregam datas e distorcem o lead time (b). | Lead time (b) ficou indisponível para 43 dos 315 repositórios (272 válidos). A troca do lead time (a) pelo (b) foi a mudança de definição que **mais alterou** a classificação (C1×C3: 23,6% mudaram, κ = 0,673). | Reportado como sensibilidade na RQ07. |
| C6 | **Tempo de recuperação baseado em CI.** "Recuperação" = intervalo entre um run com falha e o próximo sucesso no default branch, não o restabelecimento de um serviço. | 7.062 episódios em 289 repositórios; **1,1%** censurados (sem sucesso posterior na janela). Mediana KM = 4,37 h. | Censura tratada com Kaplan-Meier (`analysis/recovery_survival.py`), sem descartar episódios. |

## 2. Validade interna — há fatores não controlados que explicam os resultados?

| # | Ameaça | Evidência no estudo | Mitigação / impacto |
|---|---|---|---|
| I1 | **Idade do repositório como confundidor.** Repositórios mais novos lançam mais releases, mais rápido e com mais patches. | RQ06: idade tem os maiores efeitos do estudo: lead time (ε² = **0,266**), CFR(b) (ε² = **0,277**) e deployment frequency (ε² = 0,120), todos significativos após Holm. O quartil mais novo tem lead time mediano de 18 h contra 556 h no mais antigo (δ de Cliff = −0,75). | Diferenças atribuídas a linguagem ou popularidade podem ser parcialmente efeito da idade. Não houve controle multivariado; a RQ06 é **associativa**, não causal. |
| I2 | **Composição de linguagens.** Os grupos de linguagem diferem em idade e tipo de projeto (TypeScript e Rust concentram projetos mais novos e com releases frequentes). | Linguagem associada a DF, lead time e CFR(b) (ε² 0,06–0,10). | Mesma ressalva de I1: as associações não isolam o efeito da linguagem. |
| I3 | **Práticas de release heterogêneas.** Monorepos com várias tags por pacote, releases automáticas por bot e pré-releases mudam a contagem de deploys sem refletir mudança de desempenho. | Exemplos na amostra: `0no-co/gql.tada` (151 releases, várias por pacote), `0xPlaygrounds/rig` (636 releases). | Pré-releases ficam fora de C1; o efeito das tags é medido na RQ07. Não há deduplicação por pacote. |
| I4 | **Mudança de amostra entre coletas.** A amostra foi recoletada no commit `ef9a837` (#74) para fixar o corte (311 → 315 repositórios). | `config.toml` declara `final_sample_size = 315`, mas `reports/funnel.md` ainda mostra o funil da coleta anterior (1600 → 311). | **Pendente:** regenerar `funnel.md` com a coleta atual para manter a rastreabilidade. |

## 3. Validade externa — os resultados valem além da amostra?

| # | Ameaça | Evidência no estudo | Mitigação / impacto |
|---|---|---|---|
| E1 | **Projetos populares e open-source ≠ projetos corporativos.** A amostra exige ≥ 100 estrelas, ≥ 5 releases e ≥ 50 workflow runs na janela. | Funil: de 1.600 candidatos, ~76% foram descartados por terem < 5 releases. A amostra representa projetos **ativos e com release formal**, não o GitHub em geral. | As conclusões valem para projetos OSS populares, ativos, que usam GitHub Actions e releases. Não generalizar para software corporativo nem para projetos sem releases. |
| E2 | **Uma janela de 12 meses.** Janela fixa de 2025-10-01 a 2026-09-30. | Na RQ08, 77% (DF) e 83% (CFR CI) dos repositórios não tiveram tendência mensal significativa: o retrato é estável dentro da janela, mas não diz nada sobre outros períodos. | Janela fixada pelo enunciado; reportada em todos os resultados. |
| E3 | **Plataforma única.** Só GitHub e GitHub Actions; projetos com CI externa (Jenkins, GitLab CI, CircleCI) ficaram fora. | 12 repositórios descartados por não terem workflow runs válidos. | Limitação declarada. |
| E4 | **Cortes DORA fixos e adaptados.** As faixas Elite/High/Medium/Low usam cortes fixos da disciplina, não os clusters anuais do relatório DORA. | 69 dos 315 repositórios (21,9%) ficam **não classificáveis** por falta de alguma métrica. | Distribuições comparáveis só entre estudos que usam os mesmos cortes; os não classificáveis são reportados explicitamente. |

## 4. Validade de conclusão — a análise estatística é adequada?

| # | Ameaça | Evidência no estudo | Mitigação / impacto |
|---|---|---|---|
| S1 | **Comparações múltiplas.** A RQ06 testa 4 fatores × 5 métricas, mais os pós-testes de Dunn. | 20 testes de Kruskal-Wallis com correção de **Holm**; vários resultados significativos sem correção (ex.: linguagem × CFR(a), p = 0,004) deixam de ser após Holm (p = 0,051). | Holm aplicado em todas as famílias; efeitos reportados (ε², δ de Cliff), não só p-valores. |
| S2 | **Subgrupos pequenos.** O fator *tipo de projeto* só existe para a amostra-ouro rotulada. | RQ06 com tipo: n = 54 (21/21/12 por grupo); nenhum teste foi significativo após Holm, apesar de efeitos ε² até 0,08. | Ausência de significância **não** indica ausência de efeito (baixo poder). Declarado como limitação. |
| S3 | **Poder do Mann-Kendall com poucas observações.** | Com 4 trimestres, mesmo uma sequência perfeitamente monótona tem p ≈ 0,089: **0%** de tendências significativas. Com 12 meses, 16,8% dos repositórios têm DF crescente e 11,1% têm CFR de CI crescente. | Escala mensal reportada como principal. Os 315 testes por métrica **não** foram corrigidos para comparações múltiplas; com α = 0,05, espera-se ~16 falsos positivos por métrica, então as proporções mensais devem ser lidas com cautela. |
| S4 | **Distribuições assimétricas e outliers.** | Lead time: mediana 166 h, IQR 22,7–626 h; repositórios com centenas de releases. | Só estatística não paramétrica (mediana, IQR, Spearman, Kruskal-Wallis, Mann-Whitney); ICs por **bootstrap BCa** (2.000 réplicas, semente 42). |
| S5 | **Dados ausentes não aleatórios.** | Lead time ausente em 43 repositórios, recovery em 30; C1–C3 sem categoria para 69. Os ausentes se concentram em monorepos e em tags não comparáveis. | As análises usam os casos disponíveis e reportam o n de cada teste; não houve imputação. |

---
