import * as fs from 'fs';
import * as path from 'path';
import 'dotenv/config';
import YAML from 'yaml';
import jp from 'jsonpath';
import { Parser } from 'json2csv';

import { ProviderFactory } from './providers/factory';
import { GitHubGraphQLProvider } from './providers/github-graphql';
import { JobSpecification } from './core/interfaces/spec';

// 1. Registro de Providers Disponíveis na Factory
const GITHUB_PERSONAL_ACCESS_TOKEN = process.env.GITHUB_PERSONAL_ACCESS_TOKEN;

if (!GITHUB_PERSONAL_ACCESS_TOKEN) {
  console.error('❌ ERRO: O token do GitHub não foi configurado nas variáveis de ambiente.');
  process.exit(1);
}

// Registra os adaptadores conhecidos
ProviderFactory.register('github-graphql', new GitHubGraphQLProvider(GITHUB_PERSONAL_ACCESS_TOKEN));
// Futuramente quando criarem o GitLab/REST:
// ProviderFactory.register('gitlab-rest', new GitLabRestProvider(process.env.GITLAB_TOKEN));

/**
 * Função utilitária para carregar e parsear uma Spec YAML
 */
function loadSpec(filePath: string): JobSpecification {
  const absolutePath = path.resolve(filePath);
  const fileContent = fs.readFileSync(absolutePath, 'utf8');
  return YAML.parse(fileContent) as JobSpecification;
}

/**
 * Normalizador/Extrator Genérico usando as regras de JSONPath da Spec
 */
function extractMetrics(rawData: any, rules: JobSpecification['extractionRules']) {
  const extracted: Record<string, any> = {};

  for (const rule of rules) {
    // jp.query extrai o valor baseado na expressão JSONPath (ex: "$.search.nodes")
    const result = jp.query(rawData, rule.jsonPath);
    
    // Se o resultado for uma lista com 1 elemento, descompacta para o objeto final
    extracted[rule.metricName] = result.length === 1 ? result[0] : result;
  }

  return extracted;
}

/**
 * Utilitário para achatar o JSON retornado do GitHub e salvar em CSV dentro de /data
 */
function saveToCsv(dataList: any[], outputFileName: string) {
  if (!dataList || dataList.length === 0) {
    console.log('⚠️ Nenhum dado para exportar para CSV.');
    return;
  }

  // 1. Garante que o diretório /data existe
  const dataDir = path.resolve('./data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  // 2. Converte JSON -> CSV
  const json2csvParser = new Parser();
  const csvContent = json2csvParser.parse(dataList);

  // 3. Grava o arquivo na pasta ./data/
  const outputPath = path.join(dataDir, outputFileName);
  fs.writeFileSync(outputPath, csvContent, 'utf8');

  console.log(`\n💾 CSV salvo com sucesso em: ${outputPath}`);
}

function flattenRepositories(repositories: any[]) {
  return repositories.map((repo: any) => {
    const totalIssues = repo.totalIssues?.totalCount || 0;
    const closedIssues = repo.closedIssues?.totalCount || 0;
    const closedIssuesRatio = totalIssues > 0 ? parseFloat((closedIssues / totalIssues).toFixed(4)) : 0;

    return {
      nome: repo.nameWithOwner,
      data_criacao: repo.createdAt,
      ultimo_push: repo.pushedAt,
      linguagem: repo.primaryLanguage?.name || 'N/A',
      merged_prs: repo.pullRequests?.totalCount || 0,
      releases: repo.releases?.totalCount || 0,
      total_issues: totalIssues,
      closed_issues: closedIssues,
      ratio_closed_issues: closedIssuesRatio,
    };
  });
}

async function run() {
  try {
    // 2. Carrega a especificação YAML desejada
    const specPath = process.argv[2] || './specs/github-search-v1.yaml';
    console.log(`📄 Carregando especificação de: ${specPath}`);
    
    const spec = loadSpec(specPath);
    console.log(`📌 Executando Spec [${spec.id}] v${spec.version} via Provider: ${spec.provider}`);

    // 3. Obtém o Provider correto através da Factory
    const provider = ProviderFactory.getProvider(spec.provider);

    // 4. Inicia a mineração (Passando o Target genérico e a Spec lida)
    const miningTarget = { owner: '', repo: '' }; // Pode ser estendido se necessário
    const iterator = provider.fetchRepositoryData(miningTarget, spec);
    const maxRepositories = 100;
    const repositories: any[] = [];

    for await (const chunk of iterator) {
      console.log(`\n✅ Chunk recebido! Rate Limit Restante: ${chunk.rateLimit.remaining}`);

      // 5. Camada 1: Salvar RAW DATA no banco (Simulado aqui por console.log)
      console.log('💾 [RAW LAYER] Resposta bruta pronta para gravação em banco/JSONB');

      // 6. Camada 2: Extração Analítica Genérica via JSONPath
      const metrics = extractMetrics(chunk.rawData, spec.extractionRules);

      console.log('\n📊 [ANALYTICS LAYER] Métricas Extraídas dinamicamente via Spec:');
      console.log(JSON.stringify(metrics, null, 2));

      const repos = metrics.repositories || [];

      for (const repo of repos) {
        repositories.push(repo);
        if (repositories.length >= maxRepositories) {
          break;
        }
      }

      if (repositories.length >= maxRepositories) {
        console.log(`\n🧮 Limite de ${maxRepositories} repositórios atingido.`);
        break;
      }
    }

    // 7. Camada 3: Exportação para CSV consolidado
    const fileName = `${spec.id}_${Date.now()}.csv`;
    saveToCsv(flattenRepositories(repositories), fileName);

    console.log('\n🚀 Execução concluída com sucesso!');
  } catch (err: any) {
    console.error('\n❌ Erro durante o pipeline de mineração:', err.message);
  }
}

run();