import 'dotenv/config';
import * as path from 'path';
import { ProviderFactory } from './providers/factory';
import { GitHubGraphQLProvider } from './providers/github-graphql';
import { loadSpec, validateSpec } from './core/spec-loader';
import { extractRecords } from './core/record-extractor';
import { buildCsvRows, saveToCsv } from './exporters/csv-exporter';

const token = process.env.GITHUB_PERSONAL_ACCESS_TOKEN;

async function run(): Promise<void> {
  if (!token) throw new Error('O token do GitHub não foi configurado nas variáveis de ambiente.');

  const specPath = process.argv[2] || './specs/github-search-v2.yaml';
  const spec = loadSpec(specPath);
  validateSpec(spec);
  ProviderFactory.register('github-graphql', new GitHubGraphQLProvider(token));
  const provider = ProviderFactory.getProvider(spec.provider);
  const collectedAt = new Date();
  const records: unknown[] = [];

  console.log(`📌 Executando Spec [${spec.id}] v${spec.version} via ${spec.provider}`);
  for await (const chunk of provider.fetchRepositoryData({}, spec)) {
    console.log(`✅ Página recebida. Rate limit restante: ${chunk.rateLimit.remaining}`);
    for (const record of extractRecords(chunk.rawData, spec.collection!.recordsPath)) {
      records.push(record);
      if (records.length >= spec.collection!.maxRecords) break;
    }
    if (records.length >= spec.collection!.maxRecords) break;
  }

  const rows = buildCsvRows(records, spec.csv!.columns, collectedAt);
  const fileName = `${spec.csv!.fileNamePrefix ?? spec.id}_${Date.now()}.csv`;
  const outputPath = saveToCsv(rows, spec.csv!.columns, spec.csv!.outputDirectory ?? './data', fileName);
  console.log(outputPath ? `💾 CSV salvo em: ${path.resolve(outputPath)}` : '⚠️ Nenhum dado para exportar.');
}

run().catch((error: unknown) => {
  console.error('❌ Erro durante o pipeline de mineração:', error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
