import { JobSpecification, MiningTarget } from './spec';

export interface RateLimitStatus {
  remaining: number;
  resetAt: Date;
  cost?: number;
}

export interface MiningChunk {
  rawData: any;                       // Resposta bruta da API (JSON/Object)
  rateLimit: RateLimitStatus;
  target: MiningTarget;
  specId: string;
}

export interface IMiningProvider {
  /**
   * Identificador único da plataforma/protocolo (ex: 'github-graphql')
   */
  readonly name: string;

  /**
   * Executa a busca paginada no alvo e emite páginas de dados à medida que chegam.
   */
  fetchRepositoryData(
    target: MiningTarget,
    spec: JobSpecification
  ): AsyncIterable<MiningChunk>;

  /**
   * Consulta a quota remanescente do token/API.
   */
  checkRateLimit(): Promise<RateLimitStatus>;
}