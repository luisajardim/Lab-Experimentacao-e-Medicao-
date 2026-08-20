export type ProviderType = 'github-graphql' | 'gitlab-rest' | 'bitbucket-rest';

export interface MiningTarget {
  owner?: string;
  repo?: string;
  [key: string]: any; // Parâmetros extras caso a plataforma exija (ex: projectId)
}

export interface ExtractionRule {
  metricName: string;
  jsonPath: string; // Ex: "repository.pullRequests.nodes" ou "$.[*].title"
}

export type CsvColumnType = 'string' | 'integer' | 'number' | 'date';

export interface CsvColumn {
  name: string;
  jsonPath?: string;
  type: CsvColumnType;
  default?: string | number;
  transform?: string;
  sourcePath?: string;
}

export interface CollectionConfig {
  /** JSONPath que aponta para os registros de uma página da resposta. */
  recordsPath: string;
  /** Quantidade máxima de registros a consolidar durante a execução. */
  maxRecords: number;
  /** JSONPath opcional para pageInfo quando a raiz da query não for óbvia. */
  pageInfoPath?: string;
}

export interface CsvConfig {
  outputDirectory?: string;
  fileNamePrefix?: string;
  columns: CsvColumn[];
}

export interface RestConfig {
  endpointPath: string;           // Ex: "/projects/:owner%2F:repo/merge_requests"
  httpMethod: 'GET' | 'POST';
  defaultParams?: Record<string, any>;
  paginationType: 'header_link' | 'page_number' | 'cursor';
}

export interface JobSpecification {
  id: string;
  version: string;
  provider: ProviderType;
  description?: string;
  
  // Usado se provider for GraphQL
  graphqlQuery?: string;

  // Caminho JSONPath até pageInfo quando a conexão paginada não está na raiz (ex.: Projects v2)
  pageInfoJsonPath?: string;
  
  // Usado se provider for REST
  restConfig?: RestConfig;
  
  // Regras de extração e normalização de dados
  extractionRules: ExtractionRule[];

  /** Variáveis estáticas mescladas às variáveis de paginação do provider. */
  variables?: Record<string, unknown>;
  collection?: CollectionConfig;
  csv?: CsvConfig;
}
