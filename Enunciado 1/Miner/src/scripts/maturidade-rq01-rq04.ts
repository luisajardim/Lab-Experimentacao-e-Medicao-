import * as fs from 'fs';
import * as path from 'path';
import { parseCsvToJson, type JsonRow } from './csv-to-json';
import { summarize, distribution, round, roundSummary, type MetricSummary, type Bucket } from '../core/stats';

const DEFAULT_INPUT = './data/1000_popular_repos.csv';
const DEFAULT_OUTPUT = './docs/relatorio-estatistico-rq01-rq04.md';
const TOP_OUTLIERS = 5;

const IDADE_EDGES = [1, 2, 5, 10, 15, Infinity];
const IDADE_LABELS = ['até 1 ano', '1-2 anos', '2-5 anos', '5-10 anos', '10-15 anos', '15+ anos'];

const DIAS_EDGES = [1, 7, 30, 90, 365, Infinity];
const DIAS_LABELS = ['até 1 dia', '2-7 dias', '8-30 dias', '31-90 dias', '91-365 dias', 'mais de 365 dias'];

export interface ValidationResult {
  registros: number;
  ausentesIdade: number;
  ausentesDias: number;
  negativosIdade: number;
  negativosDias: number;
}

export interface MaturityMetric {
  resumo: MetricSummary;
  faixas: Bucket[];
  maioresOutliers: Array<{ nome: string; valor: number }>;
}

export interface MaturityReportData {
  totalRepositorios: number;
  validacao: ValidationResult;
  idadeAnos: MaturityMetric;
  diasDesdeUltimaAtualizacao: MaturityMetric;
}

function topOutliers(rows: JsonRow[], column: string, summary: MetricSummary, count: number) {
  return [...rows]
    .filter((row) => Number(row[column]) > summary.upperFence)
    .sort((a, b) => Number(b[column]) - Number(a[column]))
    .slice(0, count)
    .map((row) => ({ nome: String(row.nome ?? ''), valor: round(Number(row[column])) }));
}

function validate(rows: JsonRow[]): ValidationResult {
  const isMissing = (value: unknown) => value === undefined || value === null || value === '';
  return {
    registros: rows.length,
    ausentesIdade: rows.filter((row) => isMissing(row.idade_anos)).length,
    ausentesDias: rows.filter((row) => isMissing(row.dias_desde_ultima_atualizacao)).length,
    negativosIdade: rows.filter((row) => Number(row.idade_anos) < 0).length,
    negativosDias: rows.filter((row) => Number(row.dias_desde_ultima_atualizacao) < 0).length,
  };
}

export function buildMaturityReportData(rows: JsonRow[]): MaturityReportData {
  if (rows.length === 0) {
    throw new Error('Dataset vazio: nada para analisar.');
  }

  const idadeValues = rows.map((row) => Number(row.idade_anos)).filter((value) => Number.isFinite(value));
  const diasValues = rows.map((row) => Number(row.dias_desde_ultima_atualizacao)).filter((value) => Number.isFinite(value));

  // Outliers são calculados com os limites "crus" (não arredondados), para não
  // classificar erroneamente um valor que só parece estar no limite por causa do arredondamento.
  const idadeSummaryRaw = summarize(idadeValues);
  const diasSummaryRaw = summarize(diasValues);

  return {
    totalRepositorios: rows.length,
    validacao: validate(rows),
    idadeAnos: {
      resumo: roundSummary(idadeSummaryRaw),
      faixas: distribution(idadeValues, IDADE_EDGES, IDADE_LABELS),
      maioresOutliers: topOutliers(rows, 'idade_anos', idadeSummaryRaw, TOP_OUTLIERS),
    },
    diasDesdeUltimaAtualizacao: {
      resumo: roundSummary(diasSummaryRaw),
      faixas: distribution(diasValues, DIAS_EDGES, DIAS_LABELS),
      maioresOutliers: topOutliers(rows, 'dias_desde_ultima_atualizacao', diasSummaryRaw, TOP_OUTLIERS),
    },
  };
}

function bucketTable(buckets: Bucket[]): string {
  const rows = buckets.map((bucket) => `| ${bucket.faixa} | ${bucket.contagem} | ${bucket.percentual}% |`).join('\n');
  return `| Faixa | Repositórios | % |\n|---|---:|---:|\n${rows}`;
}

function outlierTable(outliers: Array<{ nome: string; valor: number }>, valueLabel: string): string {
  if (outliers.length === 0) return '_Nenhum outlier acima do limite superior._';
  const rows = outliers.map((row) => `| ${row.nome} | ${row.valor} |`).join('\n');
  return `| Repositório | ${valueLabel} |\n|---|---:|\n${rows}`;
}

export function renderMaturityReport(data: MaturityReportData, sourceFile: string): string {
  const { idadeAnos, diasDesdeUltimaAtualizacao: dias, validacao } = data;

  return `# Relatório estatístico — Maturidade dos repositórios (RQ01 e RQ04)

**Fonte:** \`${sourceFile}\`
**Gerado em:** ${new Date().toISOString()}
**Repositórios analisados:** ${data.totalRepositorios}
**Critério de outlier:** limite de Tukey, \`Q1 - 1,5×IQR\` / \`Q3 + 1,5×IQR\`.

## Validação de consistência

| Verificação | Resultado |
|---|---:|
| Registros lidos | ${validacao.registros} |
| Valores ausentes em \`idade_anos\` | ${validacao.ausentesIdade} |
| Valores ausentes em \`dias_desde_ultima_atualizacao\` | ${validacao.ausentesDias} |
| Valores negativos em \`idade_anos\` | ${validacao.negativosIdade} |
| Valores negativos em \`dias_desde_ultima_atualizacao\` | ${validacao.negativosDias} |

Valores negativos indicariam erro de extração (idade e tempo desde o último push não podem ser negativos); valores ausentes indicariam falha ao coletar \`createdAt\`/\`pushedAt\`.

## RQ01 — Idade do repositório (anos)

| Mínimo | Q1 | Mediana | Média | Q3 | Máximo | IQR |
|---:|---:|---:|---:|---:|---:|---:|
| ${idadeAnos.resumo.minimum} | ${idadeAnos.resumo.q1} | ${idadeAnos.resumo.median} | ${idadeAnos.resumo.mean} | ${idadeAnos.resumo.q3} | ${idadeAnos.resumo.maximum} | ${idadeAnos.resumo.iqr} |

Distribuição por faixa etária:

${bucketTable(idadeAnos.faixas)}

Outliers (limite superior ${idadeAnos.resumo.upperFence} anos): **${idadeAnos.resumo.outliers}**

${outlierTable(idadeAnos.maioresOutliers, 'Idade (anos)')}

## RQ04 — Dias desde a última atualização

| Mínimo | Q1 | Mediana | Média | Q3 | Máximo | IQR |
|---:|---:|---:|---:|---:|---:|---:|
| ${dias.resumo.minimum} | ${dias.resumo.q1} | ${dias.resumo.median} | ${dias.resumo.mean} | ${dias.resumo.q3} | ${dias.resumo.maximum} | ${dias.resumo.iqr} |

Distribuição por faixa:

${bucketTable(dias.faixas)}

Outliers (limite superior ${dias.resumo.upperFence} dias): **${dias.resumo.outliers}**

${outlierTable(dias.maioresOutliers, 'Dias sem push')}
`;
}

function run(): void {
  const inputPath = process.argv[2] || DEFAULT_INPUT;
  const outputPath = process.argv[3] || DEFAULT_OUTPUT;

  const rows = parseCsvToJson(fs.readFileSync(path.resolve(inputPath), 'utf8'));
  const data = buildMaturityReportData(rows);
  const markdown = renderMaturityReport(data, inputPath);

  const resolvedOutput = path.resolve(outputPath);
  fs.mkdirSync(path.dirname(resolvedOutput), { recursive: true });
  fs.writeFileSync(resolvedOutput, markdown, 'utf8');

  console.log(`📈 Relatório de maturidade (RQ01/RQ04) gerado sobre ${rows.length} repositórios.`);
  console.log(`💾 Salvo em: ${resolvedOutput}`);
}

if (require.main === module) {
  try {
    run();
  } catch (error) {
    console.error('❌ Erro ao gerar relatório de maturidade:', error instanceof Error ? error.message : error);
    process.exitCode = 1;
  }
}
