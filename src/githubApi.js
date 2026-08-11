const GITHUB_API_URL = 'https://api.github.com/graphql';

const QUERY = `
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
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
`;

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function fetchWithRetryAndRateLimit(token, cursor = null, attempt = 1) {
  if (!token) {
    throw new Error('Personal Access Token (PAT) não fornecido.');
  }

  try {
    console.log(`[Requisicao] Buscando repositórios... (Cursor: ${cursor || 'Inicio'})`);
    
    const response = await fetch(GITHUB_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        query: QUERY,
        variables: { cursor }
      })
    });

    if (response.status === 502 || response.status >= 500) {
      throw new Error(`Erro do servidor GitHub: Status ${response.status}`);
    }

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro HTTP ${response.status}: ${errorText}`);
    }

    const data = await response.json();

    if (data.errors) {
      console.error('[GraphQL Error]', data.errors);
      throw new Error('Erro na execução da query GraphQL.');
    }

    const rateLimit = data.data?.rateLimit;
    if (rateLimit) {
      console.log(`[Rate Limit] Restante: ${rateLimit.remaining}/${rateLimit.limit} | Custo da query: ${rateLimit.cost}`);
      
      if (rateLimit.remaining <= 10) {
        const resetTime = new Date(rateLimit.resetAt).getTime();
        const now = Date.now();
        const waitTime = Math.max(0, resetTime - now) + 5000;
        console.log(`[Rate Limit] Limite crítico atingido. Aguardando ${Math.ceil(waitTime / 1000)} segundos até o reset...`);
        await delay(waitTime);
      }
    }

    return data.data;

  } catch (error) {
    console.error(`[Erro na tentativa ${attempt}]`, error.message);
    if (attempt <= 3) {
      const backoffTime = Math.pow(2, attempt) * 1000;
      console.log(`[Backoff] Tentando novamente em ${backoffTime / 1000}s...`);
      await delay(backoffTime);
      return fetchWithRetryAndRateLimit(token, cursor, attempt + 1);
    } else {
      throw new Error(`Falha definitiva após ${attempt} tentativas consecutivas: ${error.message}`);
    }
  }
}

module.exports = {
  fetchWithRetryAndRateLimit
};
