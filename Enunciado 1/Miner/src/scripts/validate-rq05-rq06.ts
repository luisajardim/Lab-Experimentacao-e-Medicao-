import * as fs from 'fs';
import * as path from 'path';

type RepoRow = {
  nome: string;
  linguagem: string;
  merged_prs: number;
  releases: number;
  total_issues: number;
  closed_issues: number;
  ratio_closed_issues: number;
  dias_desde_ultima_atualizacao: number;
};

function parseCsv(content: string): Record<string, string>[] {
  const lines = content.split(/\r?\n/).filter((line) => line.trim().length > 0);
  if (lines.length < 2) {
    return [];
  }

  const parseLine = (line: string): string[] => {
    const values: string[] = [];
    let current = '';
    let inQuotes = false;

    for (let index = 0; index < line.length; index += 1) {
      const char = line[index];
      const next = line[index + 1];

      if (char === '"' && inQuotes && next === '"') {
        current += '"';
        index += 1;
      } else if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(current);
        current = '';
      } else {
        current += char;
      }
    }

    values.push(current);
    return values;
  };

  const headers = parseLine(lines[0]).map((header) => header.replace(/^"|"$/g, ''));
  return lines.slice(1).map((line) => {
    const values = parseLine(line).map((value) => value.replace(/^"|"$/g, ''));
    const row: Record<string, string> = {};
    headers.forEach((header, index) => {
      row[header] = values[index] ?? '';
    });
    return row;
  });
}

function median(values: number[]): number {
  if (values.length === 0) {
    return 0;
  }
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  if (sorted.length % 2 === 0) {
    return (sorted[middle - 1] + sorted[middle]) / 2;
  }
  return sorted[middle];
}

function findLatestSearchCsv(dataDir: string): string {
  const requested = process.argv[2];
  if (requested) {
    return path.resolve(requested);
  }

  const files = fs.readdirSync(dataDir)
    .filter((file) => file.startsWith('github-search-v1_') && file.endsWith('.csv'))
    .map((file) => ({ file, time: fs.statSync(path.join(dataDir, file)).mtimeMs }))
    .sort((a, b) => b.time - a.time);

  if (files.length === 0) {
    throw new Error(`Nenhum CSV github-search-v1_*.csv encontrado em ${dataDir}`);
  }

  return path.join(dataDir, files[0].file);
}

function toRows(raw: Record<string, string>[]): RepoRow[] {
  return raw.map((row) => ({
    nome: row.nome,
    linguagem: row.linguagem || 'N/A',
    merged_prs: Number(row.merged_prs || 0),
    releases: Number(row.releases || 0),
    total_issues: Number(row.total_issues || 0),
    closed_issues: Number(row.closed_issues || 0),
    ratio_closed_issues: Number(row.ratio_closed_issues || 0),
    dias_desde_ultima_atualizacao: Number(row.dias_desde_ultima_atualizacao || 0)
  }));
}

function languageCounts(rows: RepoRow[]): Array<[string, number]> {
  const counts = new Map<string, number>();
  for (const row of rows) {
    counts.set(row.linguagem, (counts.get(row.linguagem) || 0) + 1);
  }
  return Array.from(counts.entries()).sort((a, b) => b[1] - a[1]);
}

function run(): void {
  const dataDir = path.resolve('./data');
  const csvPath = findLatestSearchCsv(dataDir);
  const rows = toRows(parseCsv(fs.readFileSync(csvPath, 'utf8')));

  if (rows.length === 0) {
    throw new Error(`CSV vazio: ${csvPath}`);
  }

  const ratios = rows.map((row) => row.ratio_closed_issues);
  const invalidRatio = rows.filter((row) => row.ratio_closed_issues < 0 || row.ratio_closed_issues > 1);
  const closedGtTotal = rows.filter((row) => row.closed_issues > row.total_issues);
  const zeroIssues = rows.filter((row) => row.total_issues === 0);
  const missingLanguage = rows.filter((row) => row.linguagem === 'N/A');
  const languages = languageCounts(rows);
  const octoverseTop = ['TypeScript', 'Python', 'JavaScript', 'Java', 'C#'];
  const inOctoverseTop = rows.filter((row) => octoverseTop.includes(row.linguagem)).length;

  const lines: string[] = [
    '# Validação S02 — RQ05 e RQ06',
    '',
    `Arquivo: \`${path.relative(path.resolve('.'), csvPath).replace(/\\/g, '/')}\``,
    `Repositórios no CSV: **${rows.length}**`,
    '',
    'Fonte externa de linguagens populares: **GitHub Octoverse 2025**',
    '([relatório](https://octoverse.github.com/), [post oficial](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)).',
    'Ranking usado (por contribuidores, agosto/2025): 1) TypeScript 2) Python 3) JavaScript 4) Java 5) C#.',
    '',
    '## RQ05 — Linguagem primária',
    '',
    `| Linguagem | Contagem | % |`,
    `|---|---:|---:|`
  ];

  for (const [language, count] of languages.slice(0, 15)) {
    const pct = ((count / rows.length) * 100).toFixed(1);
    lines.push(`| ${language} | ${count} | ${pct}% |`);
  }

  lines.push(
    '',
    `- Sem linguagem definida (N/A): ${missingLanguage.length} (${((missingLanguage.length / rows.length) * 100).toFixed(1)}%)`,
    `- Repositórios nas 5 linguagens do Octoverse 2025: ${inOctoverseTop} (${((inOctoverseTop / rows.length) * 100).toFixed(1)}%)`,
    '',
    '## RQ06 — Razão de issues fechadas',
    '',
    `| Métrica | Valor |`,
    `|---|---|`,
    `| Mínimo | ${Math.min(...ratios).toFixed(4)} |`,
    `| Mediana | ${median(ratios).toFixed(4)} |`,
    `| Máximo | ${Math.max(...ratios).toFixed(4)} |`,
    `| Repositórios sem issues (total = 0) | ${zeroIssues.length} |`,
    `| Razão fora de [0, 1] | ${invalidRatio.length} |`,
    `| closed_issues > total_issues | ${closedGtTotal.length} |`,
    '',
    '## Outliers e observações',
    ''
  );

  if (zeroIssues.length > 0) {
    lines.push('Repositórios com 0 issues (aba desabilitada ou sem histórico):');
    for (const row of zeroIssues.slice(0, 15)) {
      lines.push(`- ${row.nome} (${row.linguagem})`);
    }
    lines.push('');
  }

  if (invalidRatio.length === 0 && closedGtTotal.length === 0) {
    lines.push('Nenhuma inconsistência numérica encontrada em `ratio_closed_issues`.');
  } else {
    lines.push('Inconsistências encontradas — revisar extração GraphQL antes de usar o dataset na análise da S03.');
  }

  const outputPath = path.resolve('./docs/rq05-rq06-validation-s02.md');
  fs.writeFileSync(outputPath, `${lines.join('\n')}\n`, 'utf8');
  console.log(lines.join('\n'));
  console.log(`\n💾 Validação gravada em: ${outputPath}`);
}

run();
