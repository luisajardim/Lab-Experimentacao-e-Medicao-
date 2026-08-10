import { IMiningProvider, MiningChunk, RateLimitStatus } from '@/core/interfaces/provider';
import { JobSpecification, MiningTarget } from '@/core/interfaces/spec';

export class GitHubGraphQLProvider implements IMiningProvider {
  readonly name = 'github-graphql';

  constructor(private readonly apiToken: string) {}

  async *fetchRepositoryData(
    target: MiningTarget,
    spec: JobSpecification
  ): AsyncIterable<MiningChunk> {
    // TODO: Implementar chamada de fato com cliente GraphQL e controle de cursor
    
    // YIELD simulado apenas para respeitar o contrato da interface
    yield {
      rawData: {},
      rateLimit: { remaining: 5000, resetAt: new Date() },
      target,
      specId: spec.id
    };
  }

  async checkRateLimit(): Promise<RateLimitStatus> {
    // TODO: Query inicial do rateLimit
    return { remaining: 5000, resetAt: new Date() };
  }
}