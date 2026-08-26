import * as fs from 'fs';
import * as path from 'path';
import { parseCsvToJson, type JsonRow } from './csv-to-json';
import { summarize, round, roundSummary, type MetricSummary } from '../core/stats';

const NUMERIC_METRICS = [
  { column: 'idade_anos', rq: 'RQ01', label: 'Idade do repositório (anos)' },
  { column: 'dias_desde_ultima_atualizacao', rq: 'RQ04', label: 'Dias desde a última atualização' },
  { column: 'total_pr_aceitas', rq: 'RQ02', label: 'Pull requests aceitas (merged)' },
  { column: 'total_releases', rq: 'RQ03', label: 'Releases' },
  { column: 'total_issues', rq: 'RQ06', label: 'Total de issues' },
  { column: 'total_issues_fechadas', rq: 'RQ06', label: 'Issues fechadas' },
  { column: 'razao_issues_fechadas', rq: 'RQ06', label: 'Razão de issues fechadas' },
] as const;

const TOP_LANGUAGES_FOR_CROSS_TAB = 5;
const DEFAULT_INPUT = './data/1000_popular_repos.csv';
const DEFAULT_OUTPUT = './data/metrics_summary.json';

type MetricEntry = MetricSummary & { rq: string; label: string };

function languageOf(row: JsonRow): string {
  const value = row.linguagem;
  return typeof value === 'string' && value.length > 0 ? value : 'N/A';
}

function languageDistribution(rows: JsonRow[]): Array<{ linguagem: string; contagem: number; percentual: number }> {
  const counts = new Map<string, number>();
  for (const row of rows) {
    const language = languageOf(row);
    counts.set(language, (counts.get(language) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([linguagem, contagem]) => ({
      linguagem,
      contagem,
      percentual: round((contagem / rows.length) * 100, 1),
    }));
}

function crossTabByLanguage(rows: JsonRow[], languages: string[]) {
  return languages.map((language) => {
    const subset = rows.filter((row) => languageOf(row) === language);
    const values = (column: string) => subset.map((row) => Number(row[column])).filter((value) => Number.isFinite(value));
    return {
      linguagem: language,
      repositorios: subset.length,
      pr_aceitas_mediana: round(summarize(values('total_pr_aceitas')).median),
      releases_mediana: round(summarize(values('total_releases')).median),
      idade_anos_mediana: round(summarize(values('idade_anos')).median),
      dias_desde_ultima_atualizacao_mediana: round(summarize(values('dias_desde_ultima_atualizacao')).median),
    };
  });
}

export function buildMetricsSummary(rows: JsonRow[]) {
  if (rows.length === 0) {
    throw new Error('Dataset vazio: nada para analisar.');
  }

  const metricas: Record<string, MetricEntry> = {};
  for (const { column, rq, label } of NUMERIC_METRICS) {
    const values = rows.map((row) => Number(row[column])).filter((value) => Number.isFinite(value));
    if (values.length === 0) {
      throw new Error(`Coluna numérica ausente ou vazia no CSV: ${column}`);
    }
    metricas[column] = { rq, label, ...roundSummary(summarize(values)) };
  }

  const rq05Linguagens = languageDistribution(rows);
  const topLanguages = rq05Linguagens.slice(0, TOP_LANGUAGES_FOR_CROSS_TAB).map((entry) => entry.linguagem);

  return {
    geradoEm: new Date().toISOString(),
    totalRepositorios: rows.length,
    metricas,
    rq05_linguagens: rq05Linguagens,
    rq07_cruzamentoPorLinguagem: crossTabByLanguage(rows, topLanguages),
  };
}

function run(): void {
  const inputPath = process.argv[2] || DEFAULT_INPUT;
  const outputPath = process.argv[3] || DEFAULT_OUTPUT;

  const resolvedInput = path.resolve(inputPath);
  const rows = parseCsvToJson(fs.readFileSync(resolvedInput, 'utf8'));
  const summary = buildMetricsSummary(rows);

  const resolvedOutput = path.resolve(outputPath);
  fs.mkdirSync(path.dirname(resolvedOutput), { recursive: true });
  fs.writeFileSync(resolvedOutput, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

  console.log(`📊 Análise estatística concluída sobre ${rows.length} repositórios (${inputPath}).`);
  console.log(`💾 Métricas consolidadas salvas em: ${resolvedOutput}`);
}

if (require.main === module) {
  try {
    run();
  } catch (error) {
    console.error('❌ Erro na análise estatística:', error instanceof Error ? error.message : error);
    process.exitCode = 1;
  }
}
