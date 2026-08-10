export type ProviderType = 'github-graphql' | 'gitlab-rest' | 'bitbucket-rest';

export interface MiningTarget {
  owner: string;
  repo: string;
  [key: string]: any; // Parâmetros extras caso a plataforma exija (ex: projectId)
}

export interface ExtractionRule {
  metricName: string;
  jsonPath: string; // Ex: "repository.pullRequests.nodes" ou "$.[*].title"
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
  
  // Usado se provider for REST
  restConfig?: RestConfig;
  
  // Regras de extração e normalização de dados
  extractionRules: ExtractionRule[];
}