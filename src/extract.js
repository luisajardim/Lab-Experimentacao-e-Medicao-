const { fetchWithRetryAndRateLimit } = require('./githubApi');

const TOKEN = process.env.TOKEN; 

async function runExtraction() {
  if (!TOKEN) {
    console.error('ERRO: O token do GitHub não foi configurado na variável de ambiente TOKEN.');
    process.exit(1);
  }

  let hasNextPage = true;
  let endCursor = null;
  const allRepos = [];
  let pageCount = 0;
  const MAX_PAGES = 1;

  console.log('Iniciando coleta de dados (Lab01S01 - 100 Repositórios)...');

  try {
    while (hasNextPage && pageCount < MAX_PAGES) {
      pageCount++;
      const data = await fetchWithRetryAndRateLimit(TOKEN, endCursor);
      
      const searchResult = data?.search;
      if (!searchResult) {
        throw new Error('Resposta GraphQL inválida ou vazia.');
      }

      const repos = searchResult.nodes;
      
      for (const repo of repos) {
        const totalIssues = repo.totalIssues?.totalCount || 0;
        const closedIssues = repo.closedIssues?.totalCount || 0;
        
        let closedIssuesRatio = 0;
        if (totalIssues > 0) {
          closedIssuesRatio = parseFloat((closedIssues / totalIssues).toFixed(4));
        }

        const extractedRepo = {
          nameWithOwner: repo.nameWithOwner,
          createdAt: repo.createdAt,
          pushedAt: repo.pushedAt,
          primaryLanguage: repo.primaryLanguage?.name || 'N/A',
          pullRequestsMerged: repo.pullRequests?.totalCount || 0,
          releases: repo.releases?.totalCount || 0,
          totalIssues: totalIssues,
          closedIssues: closedIssues,
          closedIssuesRatio: closedIssuesRatio
        };

        allRepos.push(extractedRepo);
      }

      hasNextPage = searchResult.pageInfo.hasNextPage;
      endCursor = searchResult.pageInfo.endCursor;
    }

    console.log(`\nColeta concluída com sucesso! Total processado: ${allRepos.length}`);
    console.log('\n--- Amostra de 2 Repositórios ---');
    console.log(JSON.stringify(allRepos.slice(0, 2), null, 2));

  } catch (error) {
    console.error('\nErro crítico durante a extração:', error.message);
    process.exit(1);
  }
}

runExtraction();
