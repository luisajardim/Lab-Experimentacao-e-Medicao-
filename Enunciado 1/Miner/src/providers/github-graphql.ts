import { IMiningProvider, MiningChunk, RateLimitStatus } from '@/core/interfaces/provider';
import { JobSpecification, MiningTarget } from '@/core/interfaces/spec';
import jp from 'jsonpath';

const GITHUB_API_URL = 'https://api.github.com/graphql';

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

function readJsonPath(source: Record<string, unknown>, jsonPath: string): any {
  const parts = jsonPath.replace(/^\$\.?/, '').split('.');
  let current: any = source;

  for (const part of parts) {
    if (current == null) {
      return undefined;
    }
    current = current[part];
  }

  return current;
}

function resolvePageInfo(payload: Record<string, unknown>, pageInfoJsonPath?: string): { hasNextPage: boolean; endCursor: string | null } | null {
  if (pageInfoJsonPath) {
    return readJsonPath(payload, pageInfoJsonPath) ?? null;
  }

  const rootKeys = Object.keys(payload).filter((key) => key !== 'rateLimit');
  const rootKey = rootKeys[0];
  return rootKey && (payload as any)[rootKey]?.pageInfo ? (payload as any)[rootKey].pageInfo : null;
}

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
            variables: { ...spec.variables, ...target, cursor: endCursor } // Variáveis declaradas na spec + cursor
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
          const messages = data.errors
            .map((error: { message?: string; type?: string }) => {
              const typeLabel = error.type ? `${error.type}: ` : '';
              return `${typeLabel}${error.message ?? 'erro desconhecido'}`;
            })
            .join(' | ');
          throw new Error(`Erro GraphQL: ${messages}`);
        }

        if (!data.data) {
          throw new Error('Resposta GraphQL sem campo data.');
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
        const pageInfo = spec.collection?.pageInfoPath
          ? jp.query(data.data, spec.collection.pageInfoPath)[0]
          : rootKey && data.data[rootKey]?.pageInfo ? data.data[rootKey].pageInfo : null;

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

        const isSemanticError = typeof error.message === 'string' && (
          error.message.includes('Erro GraphQL') ||
          error.message.includes('INSUFFICIENT_SCOPES') ||
          error.message.includes('Personal Access Token')
        );

        if (isSemanticError) {
          throw error;
        }

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
