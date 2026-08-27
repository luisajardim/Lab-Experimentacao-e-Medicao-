import Papa from 'papaparse';

export interface RepoRow {
  name: string;
  linguagem: string;
  merged_prs: number;
  releases: number;
  idade_anos: number;
  dias_desde_ultima_atualizacao: number;
  total_issues: number;
  closed_issues: number;
  ratio_closed_issues: number;
  [key: string]: any;
}

const repositoriesUrl = '/data/repos.json';
const rq02rq03Url = '/data/rq02-rq03.json';

export async function loadAllData(): Promise<RepoRow[]> {
  const response = await fetch(repositoriesUrl);
  if (!response.ok) throw new Error(`Não foi possível carregar os repositórios (${response.status}).`);
  const rows: Record<string, unknown>[] = await response.json();
  return rows.map((row) => ({
    name: String(row.nome || ''),
    linguagem: String(row.linguagem || 'Unknown'),
    merged_prs: Number(row.total_pr_aceitas || 0),
    releases: Number(row.total_releases || 0),
    idade_anos: Number(row.idade_anos || 0),
    dias_desde_ultima_atualizacao: Number(row.dias_desde_ultima_atualizacao || 0),
    total_issues: Number(row.total_issues || 0),
    closed_issues: Number(row.total_issues_fechadas || 0),
    ratio_closed_issues: Number(row.razao_issues_fechadas || 0)
  })) as RepoRow[];
}

export async function loadRQ02RQ03Data(): Promise<{ prs: number[]; releases: number[] }> {
  const response = await fetch(rq02rq03Url);
  if (!response.ok) throw new Error(`Não foi possível carregar rq02-rq03 (${response.status}).`);
  const rows: Record<string, unknown>[] = await response.json();
  const prs = rows.map(r => Number(r.total_pr_aceitas || 0)).filter(v => isFinite(v));
  const releases = rows.map(r => Number(r.total_releases || 0)).filter(v => isFinite(v));
  return { prs, releases };
}

export function calcMedian(values: number[]): number {
  if (values.length === 0) return 0;
  const sorted = [...values].filter(v => isFinite(v)).sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

export function calcQuartiles(values: number[]) {
  const sorted = [...values].filter(v => isFinite(v)).sort((a, b) => a - b);
  const len = sorted.length;
  if (len === 0) return { q1: 0, median: 0, q3: 0 };

  const median = calcMedian(sorted);
  const lowerHalf = sorted.slice(0, Math.floor(len / 2));
  const upperHalf = len % 2 === 0 ? sorted.slice(Math.floor(len / 2)) : sorted.slice(Math.floor(len / 2) + 1);

  return {
    q1: calcMedian(lowerHalf),
    median,
    q3: calcMedian(upperHalf)
  };
}

export function langCounts(data: RepoRow[]) {
  const counts: Record<string, number> = {};
  data.forEach(r => {
    const l = r.linguagem;
    if (l && l !== 'Unknown') {
      counts[l] = (counts[l] || 0) + 1;
    }
  });
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .map(([label, count]) => ({ label, count }));
}

export function crossTabRQ07(data: RepoRow[], topLangs: string[]) {
  return topLangs.map(lang => {
    const subset = data.filter(r => r.linguagem === lang);
    return {
      linguagem: lang,
      repos: subset.length,
      prs: calcMedian(subset.map(r => r.merged_prs)),
      releases: calcMedian(subset.map(r => r.releases)),
      idade: calcMedian(subset.map(r => r.idade_anos)),
      atualizacao: calcMedian(subset.map(r => r.dias_desde_ultima_atualizacao))
    };
  });
}

export interface SnapshotRow {
  sprint: string;
  snapshot_at: string;
  project_title: string;
  project_number: string;
  project_url: string;
  item_id: string;
  content_type: string;
  issue_number: string;
  title: string;
  issue_state: string;
  status: string;
  assignees: string;
  url: string;
  item_updated_at: string;
}

export async function loadSnapshotData(): Promise<SnapshotRow[]> {
  const response = await fetch('/data/snapshot.csv');
  if (!response.ok) throw new Error('Falha ao carregar snapshot.csv');
  const text = await response.text();
  
  return new Promise((resolve, reject) => {
    Papa.parse<SnapshotRow>(text, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        resolve(results.data as SnapshotRow[]);
      },
      error: (error: any) => reject(error)
    });
  });
}
