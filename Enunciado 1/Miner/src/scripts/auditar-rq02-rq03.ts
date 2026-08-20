import * as fs from 'fs';
import * as path from 'path';

type CsvRow = Record<string, string>;
type MetricSummary = {
  minimum: number;
  q1: number;
  median: number;
  mean: number;
  q3: number;
  maximum: number;
  iqr: number;
  upperFence: number;
};

const REQUIRED_COLUMNS = ['nome', 'total_pr_aceitas', 'total_releases'];
const DEFAULT_OUTPUT = './src/scripts/audits/auditoria_rq02_rq03.md';

function findLatestCollection(): string {
  const directory = path.resolve('./data');
  const candidates = fs.readdirSync(directory)
    .filter((file: string) => /^github-rq2-rq3-v2_.*\.csv$/.test(file))
    .map((file: any) => path.join(directory, file))
    .sort((first: any, second: any) => fs.statSync(second).mtimeMs - fs.statSync(first).mtimeMs);
  if (!candidates[0]) {
    throw new Error('Nenhum CSV github-rq2-rq3-v2 foi encontrado em ./data. Informe o arquivo como primeiro argumento.');
  }
  return candidates[0];
}

function parseCsv(content: string): CsvRow[] {
  const rows: string[][] = [];
  let row: string[] = [];
  let value = '';
  let quoted = false;

  for (let index = 0; index < content.length; index++) {
    const char = content[index];
    if (char === '"') {
      if (quoted && content[index + 1] === '"') {
        value += '"';
        index++;
      } else quoted = !quoted;
    } else if (char === ',' && !quoted) {
      row.push(value);
      value = '';
    } else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && content[index + 1] === '\n') index++;
      row.push(value);
      if (row.some((cell) => cell.length > 0)) rows.push(row);
      row = [];
      value = '';
    } else value += char;
  }
  if (value.length > 0 || row.length > 0) {
    row.push(value);
    rows.push(row);
  }

  const [headers, ...data] = rows;
  if (!headers) throw new Error('CSV vazio.');
  return data.map((cells) => Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ''])));
}

function percentile(sorted: number[], position: number): number {
  const index = (sorted.length - 1) * position;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  return lower === upper ? sorted[lower] : sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower);
}

function summarize(values: number[]): MetricSummary {
  const sorted = [...values].sort((a, b) => a - b);
  const q1 = percentile(sorted, 0.25);
  const q3 = percentile(sorted, 0.75);
  const iqr = q3 - q1;
  return {
    minimum: sorted[0],
    q1,
    median: percentile(sorted, 0.5),
    mean: values.reduce((sum, value) => sum + value, 0) / values.length,
    q3,
    maximum: sorted.at(-1)!,
    iqr,
    upperFence: q3 + 1.5 * iqr,
  };
}

function format(value: number): string {
  return Number.isInteger(value) ? String(value) : value.toFixed(2);
}

function topRows(rows: CsvRow[], metric: string, count: number): CsvRow[] {
  return [...rows].sort((a, b) => Number(b[metric]) - Number(a[metric])).slice(0, count);
}

function table(rows: CsvRow[], metric: string): string {
  return rows.map((row) => `| ${row.nome} | ${row[metric]} |`).join('\n');
}

function audit(inputPath: string, outputPath: string): void {
  const rows = parseCsv(fs.readFileSync(inputPath, 'utf8'));
  const missingColumns = REQUIRED_COLUMNS.filter((column) => !Object.hasOwn(rows[0] ?? {}, column));
  if (missingColumns.length) throw new Error(`CSV incompatível; colunas ausentes: ${missingColumns.join(', ')}.`);

  const names = new Set<string>();
  const duplicates = new Set<string>();
  const invalid: Record<string, number> = { total_pr_aceitas: 0, total_releases: 0 };
  const validRows: CsvRow[] = [];
  for (const row of rows) {
    if (names.has(row.nome)) duplicates.add(row.nome);
    names.add(row.nome);
    let isValid = Boolean(row.nome);
    for (const metric of Object.keys(invalid)) {
      const value = Number(row[metric]);
      if (!Number.isInteger(value) || value < 0 || ['undefined', 'null', ''].includes(row[metric])) {
        invalid[metric]++;
        isValid = false;
      }
    }
    if (isValid) validRows.push(row);
  }
  if (!validRows.length) throw new Error('Não há registros válidos para auditoria.');

  const prs = validRows.map((row) => Number(row.total_pr_aceitas));
  const releases = validRows.map((row) => Number(row.total_releases));
  const prSummary = summarize(prs);
  const releaseSummary = summarize(releases);
  const prOutliers = validRows.filter((row) => Number(row.total_pr_aceitas) > prSummary.upperFence);
  const releaseOutliers = validRows.filter((row) => Number(row.total_releases) > releaseSummary.upperFence);
  const zeroReleases = validRows.filter((row) => Number(row.total_releases) === 0);
  const source = path.relative(path.dirname(outputPath), inputPath);

  const markdown = `# Auditoria de Consistência e Outliers — RQ02 e RQ03

**Fonte auditada:** \`${source}\`  
**Data de execução:** ${new Date().toISOString()}  
**Critério de outlier:** limite superior de Tukey, \`Q3 + 1,5 × IQR\`.

## Integridade dos dados

| Verificação | Resultado |
| --- | ---: |
| Registros lidos | ${rows.length} |
| Registros válidos | ${validRows.length} |
| Valores inválidos em total_pr_aceitas | ${invalid.total_pr_aceitas} |
| Valores inválidos em total_releases | ${invalid.total_releases} |
| Nomes de repositório duplicados | ${duplicates.size} |
| Repositórios com zero releases | ${zeroReleases.length} (${format((zeroReleases.length / validRows.length) * 100)}%) |

Valores inválidos incluem campos vazios, null, undefined, não inteiros, negativos ou não numéricos. Repositórios sem releases são válidos: representam projetos que não usam o mecanismo de Releases do GitHub.

## Estatísticas descritivas

| Métrica | Mínimo | Q1 | Mediana | Média | Q3 | Máximo |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PRs aceitas | ${format(prSummary.minimum)} | ${format(prSummary.q1)} | ${format(prSummary.median)} | ${format(prSummary.mean)} | ${format(prSummary.q3)} | ${format(prSummary.maximum)} |
| Releases | ${format(releaseSummary.minimum)} | ${format(releaseSummary.q1)} | ${format(releaseSummary.median)} | ${format(releaseSummary.mean)} | ${format(releaseSummary.q3)} | ${format(releaseSummary.maximum)} |

## Outliers

| Métrica | IQR | Limite superior | Quantidade de outliers |
| --- | ---: | ---: | ---: |
| PRs aceitas | ${format(prSummary.iqr)} | ${format(prSummary.upperFence)} | ${prOutliers.length} |
| Releases | ${format(releaseSummary.iqr)} | ${format(releaseSummary.upperFence)} | ${releaseOutliers.length} |

### Dez maiores valores de PRs aceitas

| Repositório | PRs aceitas |
| --- | ---: |
${table(topRows(validRows, 'total_pr_aceitas', 10), 'total_pr_aceitas')}

### Dez maiores valores de releases

| Repositório | Releases |
| --- | ---: |
${table(topRows(validRows, 'total_releases', 10), 'total_releases')}

## Conclusão da auditoria

Os valores passaram pelas regras de consistência acima. Os outliers foram preservados, pois são observações reais de repositórios populares; entretanto, tornam a média sensível a poucos projetos muito ativos. Por isso, a mediana deve ser a medida central prioritária na análise das RQs 02 e 03, acompanhada da distribuição e da discussão dos valores extremos.
`;

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, markdown, 'utf8');
  console.log(`Auditoria concluída: ${outputPath}`);
}

const inputPath = process.argv[2] || findLatestCollection();
const outputPath = process.argv[3] || DEFAULT_OUTPUT;
audit(inputPath, outputPath);
