import * as fs from 'fs';
import * as path from 'path';
import 'dotenv/config';
import YAML from 'yaml';
import jp from 'jsonpath';
import { Parser } from 'json2csv';

import { ProviderFactory } from '../providers/factory';
import { GitHubGraphQLProvider } from '../providers/github-graphql';
import { JobSpecification } from '../core/interfaces/spec';

const GITHUB_PERSONAL_ACCESS_TOKEN = process.env.GITHUB_PERSONAL_ACCESS_TOKEN;

if (!GITHUB_PERSONAL_ACCESS_TOKEN) {
  console.error('❌ ERRO: O token do GitHub não foi configurado nas variáveis de ambiente.');
  process.exit(1);
}

ProviderFactory.register('github-graphql', new GitHubGraphQLProvider(GITHUB_PERSONAL_ACCESS_TOKEN));

type SnapshotRow = {
  sprint: string;
  snapshot_at: string;
  project_title: string;
  project_number: number | string;
  project_url: string;
  item_id: string;
  content_type: string;
  issue_number: string | number;
  title: string;
  issue_state: string;
  status: string;
  assignees: string;
  url: string;
  item_updated_at: string;
};

function loadSpec(filePath: string): JobSpecification {
  const absolutePath = path.resolve(filePath);
  const fileContent = fs.readFileSync(absolutePath, 'utf8');
  return YAML.parse(fileContent) as JobSpecification;
}

function uniqueLogins(values: Array<{ login?: string } | undefined>): string {
  const logins = values
    .map((node) => node?.login)
    .filter((login): login is string => Boolean(login));
  return Array.from(new Set(logins)).join(';');
}

function flattenProjectItems(rawData: any, sprint: string, snapshotAt: string): SnapshotRow[] {
  const project = rawData?.user?.projectV2 ?? rawData?.organization?.projectV2;
  const items = jp.query(rawData, '$..items.nodes[*]').filter((item: any) => item?.id);

  if (!project) {
    return [];
  }

  return items.map((item: any) => {
    const content = item.content ?? {};
    const statusFromNamedField = item.fieldValueByName?.name;
    const statusFromFieldValues = (item.fieldValues?.nodes ?? [])
      .find((node: any) => node?.field?.name === 'Status')?.name;
    const assigneeField = (item.fieldValues?.nodes ?? [])
      .find((node: any) => node?.field?.name === 'Assignees' || node?.users);
    const contentAssignees = content.assignees?.nodes ?? [];
    const projectAssignees = assigneeField?.users?.nodes ?? [];

    return {
      sprint,
      snapshot_at: snapshotAt,
      project_title: project.title ?? '',
      project_number: project.number ?? '',
      project_url: project.url ?? '',
      item_id: item.id,
      content_type: content.__typename || item.type || '',
      issue_number: content.number ?? '',
      title: content.title ?? '',
      issue_state: content.state ?? '',
      status: statusFromNamedField || statusFromFieldValues || '',
      assignees: uniqueLogins([...contentAssignees, ...projectAssignees]),
      url: content.url ?? '',
      item_updated_at: item.updatedAt ?? ''
    };
  });
}

function saveSnapshotCsv(rows: SnapshotRow[], sprint: string, snapshotAt: Date): string {
  if (rows.length === 0) {
    throw new Error(
      'Nenhum item retornado pelo Project. Confira GITHUB_PROJECT_OWNER, GITHUB_PROJECT_NUMBER, GITHUB_PROJECT_OWNER_TYPE e se o token tem o escopo read:project.'
    );
  }

  const snapshotsDir = path.resolve('./data/snapshots');
  if (!fs.existsSync(snapshotsDir)) {
    fs.mkdirSync(snapshotsDir, { recursive: true });
  }

  const parser = new Parser({ header: true });
  const csvContent = parser.parse(rows);
  const stamp = snapshotAt.toISOString().replace(/[:.]/g, '-');
  const sprintFile = path.join(snapshotsDir, `${sprint}_${stamp}.csv`);
  fs.writeFileSync(sprintFile, csvContent, 'utf8');

  const historyPath = path.join(snapshotsDir, 'history.csv');
  if (!fs.existsSync(historyPath)) {
    fs.writeFileSync(historyPath, csvContent, 'utf8');
  } else {
    const historyParser = new Parser({ header: false });
    fs.appendFileSync(historyPath, `\n${historyParser.parse(rows)}`, 'utf8');
  }

  return sprintFile;
}

async function run(): Promise<void> {
  const snapshotAt = new Date();
  const owner = process.env.GITHUB_PROJECT_OWNER || 'luisajardim';
  const ownerType = (process.env.GITHUB_PROJECT_OWNER_TYPE || 'user').toLowerCase();
  const projectNumber = Number(process.env.GITHUB_PROJECT_NUMBER || 1);
  const sprint = process.env.SPRINT_ID || 'S02';

  if (!Number.isInteger(projectNumber) || projectNumber <= 0) {
    throw new Error('GITHUB_PROJECT_NUMBER deve ser um inteiro positivo (o número do Project v2).');
  }

  const specPath = ownerType === 'organization'
    ? './specs/github-project-snapshot-org-v1.yaml'
    : './specs/github-project-snapshot-v1.yaml';

  console.log(`📄 Carregando spec de snapshot: ${specPath}`);
  console.log(`📌 Project: ${ownerType}/${owner} #${projectNumber} | sprint ${sprint}`);

  const spec = loadSpec(specPath);
  const provider = ProviderFactory.getProvider(spec.provider);
  const iterator = provider.fetchRepositoryData(
    { owner, repo: '', projectNumber },
    spec
  );

  const rows: SnapshotRow[] = [];

  for await (const chunk of iterator) {
    console.log(`\n✅ Chunk recebido! Rate Limit Restante: ${chunk.rateLimit.remaining}`);
    rows.push(...flattenProjectItems(chunk.rawData, sprint, snapshotAt.toISOString()));
  }

  const outputPath = saveSnapshotCsv(rows, sprint, snapshotAt);
  console.log(`\n💾 Snapshot salvo em: ${outputPath}`);
  console.log(`🧾 Itens exportados: ${rows.length}`);
  console.log('\n🚀 Snapshot de sprint concluído.');
}

run().catch((error: Error) => {
  console.error('\n❌ Erro durante o snapshot do GitHub Projects:', error.message);
  if (error.message.includes('read:project') || error.message.includes('INSUFFICIENT_SCOPES')) {
    console.error('➡️  Gere um PAT clássico com public_repo + read:project (ou fine-grained com Projects: Read) e atualize o .env.');
  }
  process.exit(1);
});
