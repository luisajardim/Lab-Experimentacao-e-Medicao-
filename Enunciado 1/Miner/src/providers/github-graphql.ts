import { IMiningProvider, MiningChunk, RateLimitStatus } from '@/core/interfaces/provider';
import { JobSpecification, MiningTarget } from '@/core/interfaces/spec';

const GITHUB_API_URL = 'https://api.github.com/graphql';

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export class GitHubGraphQLProvider implements IMiningProvider {
  readonly name = 'github-graphql';

  constructor(private readonly apiToken: string) {}

  async *fetchRepositoryData(
    target: MiningTarget,
    spec: JobSpecification
  ): AsyncIterable<MiningChunk> {
    if (!this.apiToken) {
      throw new Error('Personal Access Token (PAT) não fornecido ao provider.');
    }

    if (!spec.graphqlQuery) {
      throw new Error('A query GraphQL não foi fornecida na JobSpecification.');
    }

    let hasNextPage = true;
    let endCursor: string | null = null;
    let attempt = 1;

    while (hasNextPage) {
      try {
        console.log(`[Requisicao] Buscando dados GraphQL... (Cursor: ${endCursor || 'Inicio'})`);

        const response: Response = await fetch(GITHUB_API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.apiToken}`
          },
          body: JSON.stringify({
            query: spec.graphqlQuery,
            variables: { cursor: endCursor, ...target } // Passa o cursor e possíveis alvos
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

        const rateLimitRaw = data.data?.rateLimit;
        let rateLimitStatus: RateLimitStatus = { remaining: 5000, resetAt: new Date() };

        if (rateLimitRaw) {
          rateLimitStatus = {
            remaining: rateLimitRaw.remaining,
            resetAt: new Date(rateLimitRaw.resetAt),
            cost: rateLimitRaw.cost
          };
          console.log(`[Rate Limit] Restante: ${rateLimitStatus.remaining} | Custo da query: ${rateLimitStatus.cost}`);

          // Controle de proteção de quota
          if (rateLimitStatus.remaining <= 10) {
            const resetTime = rateLimitStatus.resetAt.getTime();
            const waitTime = Math.max(0, resetTime - Date.now()) + 5000;
            console.log(`[Rate Limit] Limite crítico atingido. Aguardando ${Math.ceil(waitTime / 1000)}s até o reset...`);
            await delay(waitTime);
          }
        }

        // Descobre dinamicamente a paginação independentemente do nome do rootNode ("search", "repository", etc)
        const rootKeys = Object.keys(data.data).filter(k => k !== 'rateLimit');
        const rootKey = rootKeys[0]; 
        const pageInfo = rootKey && data.data[rootKey]?.pageInfo ? data.data[rootKey].pageInfo : null;

        // Emite a página atual
        yield {
          rawData: data.data,
          rateLimit: rateLimitStatus,
          target,
          specId: spec.id
        };

        if (pageInfo) {
          hasNextPage = pageInfo.hasNextPage;
          endCursor = pageInfo.endCursor;
        } else {
          hasNextPage = false; // Se a query não for paginável (sem pageInfo), para o loop
        }

        attempt = 1; // Reseta tentativa após sucesso

      } catch (error: any) {
        console.error(`[Erro na tentativa ${attempt}]`, error.message);
        if (attempt <= 3) {
          const backoffTime = Math.pow(2, attempt) * 1000;
          console.log(`[Backoff] Tentando novamente em ${backoffTime / 1000}s...`);
          await delay(backoffTime);
          attempt++;
        } else {
          throw new Error(`Falha definitiva após ${attempt} tentativas consecutivas: ${error.message}`);
        }
      }
    }
  }

  async checkRateLimit(): Promise<RateLimitStatus> {
    const query = `
      query {
        rateLimit {
          limit
          cost
          remaining
          resetAt
        }
      }
    `;

    const response = await fetch(GITHUB_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiToken}`
      },
      body: JSON.stringify({ query })
    });

    if (!response.ok) {
      throw new Error(`Erro HTTP ${response.status} ao checar rate limit`);
    }

    const data = await response.json();
    const rl = data.data?.rateLimit;
    
    if (!rl) {
      throw new Error('Falha ao ler o rate limit do GitHub');
    }

    return {
      remaining: rl.remaining,
      resetAt: new Date(rl.resetAt),
      cost: rl.cost
    };
  }
}