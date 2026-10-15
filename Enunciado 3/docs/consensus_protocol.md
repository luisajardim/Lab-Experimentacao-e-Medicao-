# Protocolo de consenso da amostra-ouro (T13)

Este documento define como os rótulos independentes dos três integrantes
(`data/gold/labels_A.csv`, `labels_B.csv`, `labels_C.csv`) viram o rótulo de
consenso em `data/gold/labels_consensus.csv`, e registra as decisões tomadas em
reunião. O script `scripts/agreement.py` lê a tabela de decisões abaixo.

## 1. Pré-condições

- Os três arquivos estão completos e válidos
  (`python scripts/label_tool.py --validate data/gold/labels_X.csv` sem problemas).
- Cada avaliador rotulou sem consultar os demais e sem ver a saída da heurística
  (PLAN T12); a conclusão está registrada em `labels_X.audit.json`.
- A concordância é medida **antes** de qualquer discussão entre os avaliadores.

### Avaliadores

| Arquivo | Avaliador | Concluído em (UTC) |
|---|---|---|
| `labels_A.csv` | integrante do grupo (humano) | 2026-10-14 21:45 |
| `labels_B.csv` | **Claude (modelo de linguagem, Anthropic)** | 2026-10-15 19:44 |
| `labels_C.csv` | @pedroseabra27 (humano) | 2026-10-15 14:45 |

O avaliador B não é humano: como a terceira rotulagem humana não foi feita,
o modelo rotulou os mesmos dossiês (`data/gold/dossiers/`) sem acesso a
`labels_A.csv`, `labels_C.csv` ou à saída da heurística (ver
`labels_B.audit.json`). O κ deve, portanto, ser lido como concordância entre
dois humanos e um modelo, o que deve constar como limitação no relatório.

## 2. Concordância

O κ de Fleiss (`statsmodels`: `aggregate_raters` + `fleiss_kappa`) é calculado
separadamente para cada dimensão:

| Dimensão | Coluna(s) | Categorias | Itens |
|---|---|---|---|
| tipo | `project_type` | biblioteca/framework, aplicação/serviço, ferramenta CLI, outro | 1 por repositório |
| entrega | `delivers_to_user` | sim, não, incerto | 1 por repositório |
| corretiva | `corrective_1..5` | sim, não | 5 por repositório (uma por release) |

`incerto` é uma categoria própria, não um valor ausente. A interpretação segue
Landis & Koch (1977): < 0 pobre; 0,00–0,20 leve; 0,21–0,40 razoável;
0,41–0,60 moderada; 0,61–0,80 substancial; 0,81–1,00 quase perfeita.
O resultado fica em `reports/agreement.md`.

## 3. Regra de consenso

1. **Maioria simples:** se pelo menos 2 dos 3 avaliadores escolheram o mesmo
   valor, ele é o consenso. Não há discussão nesses casos, mesmo que o voto
   vencido pareça melhor.
2. **Empate 1-1-1:** só ocorre em `tipo` e `entrega` (a dimensão corretiva é
   binária, então sempre há maioria). O script lista esses itens como
   pendentes em `reports/agreement.md` e sai com código 1.
3. **Reunião de desempate:** os três integrantes discutem cada item pendente
   com base no dossiê (`data/gold/dossiers/`) e decidem um único valor válido.
   A decisão e a justificativa são registradas na tabela da seção 5.
4. Rodar `python scripts/agreement.py` de novo. O consenso está fechado
   quando o script termina com código 0 (nenhum empate pendente). A coluna
   `meeting_decisions` do CSV indica quais campos vieram da reunião.

Decisões registradas para itens que não estão empatados são ignoradas (a
maioria prevalece) e aparecem como aviso no relatório.

## 4. Reuniões realizadas

| Data | Participantes | Itens decididos | Observações |
|---|---|---:|---|
| 2026-10-15 | @luisajardim | 5 | Decisões propostas pelo Claude a partir dos dossiês e aceitas por @luisajardim. |

## 5. Decisões de desempate

Uma linha por item empatado. `coluna` é `project_type` ou `delivers_to_user`;
`decisão` deve ser um dos valores válidos da coluna.

| full_name | coluna | decisão | justificativa |
|---|---|---|---|
| BoundaryML/baml | project_type | biblioteca/framework | Usado como framework de aplicação que gera código cliente para LLMs. |
| goplus/xgo | project_type | ferramenta CLI | Linguagem distribuída e usada como toolchain de linha de comando. |
| francescopace/espectre | delivers_to_user | sim | Firmware versionado que os usuários instalam nos dispositivos. |
| openebs/openebs | delivers_to_user | incerto | Repositório guarda-chuva; os commits das releases são só docs/adopters. |
| project-chip/connectedhomeip | delivers_to_user | incerto | SDK com tags que incluem eventos de teste, não só entregas. |
