import * as fs from 'fs';
import * as path from 'path';
import { parseCsvToJson, type JsonRow } from './csv-to-json';
import { distribution, round, roundSummary, summarize, type Bucket, type MetricSummary } from '../core/stats';

const DEFAULT_INPUT = './data';
const DEFAULT_OUTPUT = './docs/stats_rq02_rq03.md';
const TOP_REPOSITORIES = 5;

const PR_BUCKETS = [100, 500, 1000, 5000, 10000, Infinity];
const PR_BUCKET_LABELS = ['até 100', '101-500', '501-1.000', '1.001-5.000', '5.001-10.000', '10.001+'];

const RELEASE_BUCKETS = [0, 1, 10, 50, 100, 500, Infinity];
const RELEASE_BUCKET_LABELS = ['0', '1', '2-10', '11-50', '51-100', '101-500', '501+'];

export interface ReportMetric {
  resumo: MetricSummary;
  faixas: Bucket[];
  maioresValores: Array<{ nome: string; valor: number }>;
}

export interface Rq02Rq03ReportData {
  totalRepositorios: number;
  repositoriosComZeroReleases: number;
  prsAceitas: ReportMetric;
  releases: ReportMetric;
}

function findLatestCollection(): string {
  const directory = path.resolve(DEFAULT_INPUT);
  const candidates = fs.readdirSync(directory)
    .filter((file: string) => /^github-rq2-rq3-v2_.*\.csv$/.test(file))
    .map((file: string) => path.join(directory, file))
    .sort((first: string, second: string) => fs.statSync(second).mtimeMs - fs.statSync(first).mtimeMs);

  if (!candidates[0]) {
    throw new Error('Nenhum CSV github-rq2-rq3-v2 foi encontrado em ./data.');
  }

  return candidates[0];
}

function topValues(rows: JsonRow[], column: string, count: number): Array<{ nome: string; valor: number }> {
  return [...rows]
    .filter((row) => Number.isFinite(Number(row[column])))
    .sort((left, right) => Number(right[column]) - Number(left[column]))
    .slice(0, count)
    .map((row) => ({ nome: String(row.nome ?? ''), valor: round(Number(row[column])) }));
}

export function buildRq02Rq03ReportData(rows: JsonRow[]): Rq02Rq03ReportData {
  if (rows.length === 0) {
    throw new Error('Dataset vazio: nada para analisar.');
  }

  const prsValues = rows.map((row) => Number(row.total_pr_aceitas)).filter((value) => Number.isFinite(value));
  const releaseValues = rows.map((row) => Number(row.total_releases)).filter((value) => Number.isFinite(value));

  if (prsValues.length === 0 || releaseValues.length === 0) {
    throw new Error('Não foi possível extrair valores numéricos de total_pr_aceitas ou total_releases.');
  }

  const prSummaryRaw = summarize(prsValues);
  const releaseSummaryRaw = summarize(releaseValues);

  return {
    totalRepositorios: rows.length,
    repositoriosComZeroReleases: rows.filter((row) => Number(row.total_releases) === 0).length,
    prsAceitas: {
      resumo: roundSummary(prSummaryRaw),
      faixas: distribution(prsValues, PR_BUCKETS, PR_BUCKET_LABELS),
      maioresValores: topValues(rows, 'total_pr_aceitas', TOP_REPOSITORIES),
    },
    releases: {
      resumo: roundSummary(releaseSummaryRaw),
      faixas: distribution(releaseValues, RELEASE_BUCKETS, RELEASE_BUCKET_LABELS),
      maioresValores: topValues(rows, 'total_releases', TOP_REPOSITORIES),
    },
  };
}

function metricTable(summary: MetricSummary): string {
  return `| Mínimo | Q1 | Mediana | Média | Q3 | Máximo | IQR | Limite superior |
|---:|---:|---:|---:|---:|---:|---:|---:|
| ${summary.minimum} | ${summary.q1} | ${summary.median} | ${summary.mean} | ${summary.q3} | ${summary.maximum} | ${summary.iqr} | ${summary.upperFence} |`;
}

function bucketTable(buckets: Bucket[]): string {
  const rows = buckets.map((bucket) => `| ${bucket.faixa} | ${bucket.contagem} | ${bucket.percentual}% |`).join('\n');
  return `| Faixa | Repositórios | % |
|---|---:|---:|
${rows}`;
}

function topTable(values: Array<{ nome: string; valor: number }>, label: string): string {
  if (values.length === 0) return '_Nenhum valor disponível._';
  const rows = values.map((row) => `| ${row.nome} | ${row.valor} |`).join('\n');
  return `| Repositório | ${label} |
|---|---:|
${rows}`;
}

export function renderRq02Rq03Report(data: Rq02Rq03ReportData, sourceFile: string): string {
  return `# Análise Estatística de Engajamento e Releases (RQ02 / RQ03)

**Fonte:** \`${sourceFile}\`
**Gerado em:** ${new Date().toISOString()}
**Repositórios analisados:** ${data.totalRepositorios}
**Critério de outlier:** limite superior de Tukey, \`Q3 + 1,5 × IQR\`.

## 1. Hipótese e objetivo

- **RQ02 — contribuição externa:** repositórios populares devem apresentar um volume relevante de PRs aceitas, mesmo que a distribuição seja muito desigual por causa de projetos grandes.
- **RQ03 — releases:** uma parte expressiva da amostra deve publicar releases, embora alguns projetos optem por distribuir versões por tags, pacotes ou imagens de container em vez de usar a funcionalidade de Releases do GitHub.

## 2. Resumo estatístico

### RQ02 — total de PRs aceitas

${metricTable(data.prsAceitas.resumo)}

**Outliers acima do limite superior:** ${data.prsAceitas.resumo.outliers}

Distribuição por faixa de PRs aceitas:

${bucketTable(data.prsAceitas.faixas)}

Top repositórios por PRs aceitas:

${topTable(data.prsAceitas.maioresValores, 'PRs aceitas')}

### RQ03 — total de releases

${metricTable(data.releases.resumo)}

**Outliers acima do limite superior:** ${data.releases.resumo.outliers}
**Repositórios sem releases (total = 0):** ${data.repositoriosComZeroReleases} (${round((data.repositoriosComZeroReleases / data.totalRepositorios) * 100, 2)}%)

Distribuição por faixa de releases:

${bucketTable(data.releases.faixas)}

Top repositórios por releases:

${topTable(data.releases.maioresValores, 'Releases')}

## 3. Interpretação

A mediana é a medida mais robusta para estas duas métricas porque a distribuição é fortemente assimétrica: a média é puxada para cima por repositórios muito grandes e ativos, enquanto a mediana mostra o comportamento central da maioria dos projetos populares.

Para **RQ02**, a mediana de ${data.prsAceitas.resumo.median} PRs aceitas mostra que a maioria dos repositórios populares tem fluxo contínuo de integração de contribuições, mas há uma cauda longa de projetos extraordinariamente ativos. Isso é consistente com ecossistemas grandes e bem mantidos, como kernels, bibliotecas de uso geral e ferramentas amplamente adotadas.

Para **RQ03**, a mediana de ${data.releases.resumo.median} releases mostra que há uma parcela relevante de projetos com histórico de publicação de versões, mas também existe uma parte importante que não usa Releases no GitHub. O fato de ${data.repositoriosComZeroReleases} repositórios (aproximadamente ${round((data.repositoriosComZeroReleases / data.totalRepositorios) * 100, 2)}%) terem zero releases reforça que a ausência de releases não é necessariamente erro de coleta — pode refletir uma estratégia de distribuição alternativa.

## 4. Conclusão

A hipótese das RQs 02 e 03 se sustenta em termos de tendência central: repositórios populares recebem contribuições relevantes e, em muitos casos, também têm histórico de lançamentos. Porém, a distribuição é muito heterogênea e a comparação deve priorizar mediana, quartis e outliers em vez de médias isoladas.
`;
}

function run(): void {
  const inputPath = process.argv[2] || findLatestCollection();
  const outputPath = process.argv[3] || DEFAULT_OUTPUT;

  const rows = parseCsvToJson(fs.readFileSync(path.resolve(inputPath), 'utf8'));
  const reportData = buildRq02Rq03ReportData(rows);
  const markdown = renderRq02Rq03Report(reportData, inputPath);

  const resolvedOutput = path.resolve(outputPath);
  fs.mkdirSync(path.dirname(resolvedOutput), { recursive: true });
  fs.writeFileSync(resolvedOutput, markdown, 'utf8');

  console.log(`📊 Relatório RQ02/RQ03 gerado sobre ${rows.length} repositórios.`);
  console.log(`💾 Salvo em: ${resolvedOutput}`);
}

if (require.main === module) {
  try {
    run();
  } catch (error) {
    console.error('❌ Erro ao gerar relatório RQ02/RQ03:', error instanceof Error ? error.message : error);
    process.exitCode = 1;
  }
}
