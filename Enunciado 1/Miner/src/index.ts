import { GitHubGraphQLProvider } from './providers/github-graphql';

const TOKEN = process.env.TOKEN;

async function runTest() {
    if (!TOKEN) {
        console.error('ERRO: O token do GitHub não foi configurado na variável de ambiente TOKEN.');
        process.exit(1);
    }

    const provider = new GitHubGraphQLProvider(TOKEN);


    const query = `
    query GetPopularRepos($cursor: String) {
      search(query: "stars:>1 sort:stars-desc", type: REPOSITORY, first: 100, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          ... on Repository {
            nameWithOwner
            createdAt
            pushedAt
            primaryLanguage {
              name
            }
            pullRequests(states: MERGED) {
              totalCount
            }
            releases {
              totalCount
            }
            closedIssues: issues(states: CLOSED) {
              totalCount
            }
            totalIssues: issues {
              totalCount
            }
          }
        }
      }
    }
  `;

    console.log('Iniciando teste da S01 com o novo Provider TypeScript...');

    const iterator = provider.fetchRepositoryData(
        {},
        {
            id: 'job-1',
            version: '1.0',
            provider: 'github-graphql',
            graphqlQuery: query,
            extractionRules: []
        }
    );

    try {
        for await (const chunk of iterator) {
            const rootKey = Object.keys(chunk.rawData).find(k => k !== 'rateLimit');
            const repos = rootKey ? chunk.rawData[rootKey].nodes : [];

            console.log(`\n✅ Sucesso! Recebemos a página via TS. Rate Limit Restante: ${chunk.rateLimit.remaining}`);

            const processedRepos = repos.map((repo: any) => {
                const totalIssues = repo.totalIssues?.totalCount || 0;
                const closedIssues = repo.closedIssues?.totalCount || 0;
                let closedIssuesRatio = 0;
                if (totalIssues > 0) {
                    closedIssuesRatio = parseFloat((closedIssues / totalIssues).toFixed(4));
                }
                return {
                    nome: repo.nameWithOwner,
                    linguagem: repo.primaryLanguage?.name || 'N/A',
                    closedIssuesRatio
                };
            });

            console.log('\n--- Amostra de 2 Repositórios formatados ---');
            console.log(JSON.stringify(processedRepos.slice(0, 2), null, 2));


            break;
        }
    } catch (err: any) {
        console.error('\nErro na extração:', err.message);
    }
}

runTest();
