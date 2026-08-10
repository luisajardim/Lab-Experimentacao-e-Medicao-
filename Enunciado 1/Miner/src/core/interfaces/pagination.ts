export interface PaginationContext {
  lastResponseData: any;
  lastHeaders: Record<string, any>;
  currentPage?: number;
  currentCursor?: string;
}

export interface NextPageParams {
  url?: string;
  params?: Record<string, any>;
}

export interface IPaginationStrategy {
  readonly type: string;
  
  /**
   * Calcula os parâmetros da próxima requisição com base no contexto anterior.
   * Retorna `null` quando não houver mais páginas a consultar.
   */
  getNextPageParams(context: PaginationContext): NextPageParams | null;
}