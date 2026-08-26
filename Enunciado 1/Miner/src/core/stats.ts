export interface MetricSummary {
  count: number;
  minimum: number;
  q1: number;
  median: number;
  mean: number;
  q3: number;
  maximum: number;
  iqr: number;
  lowerFence: number;
  upperFence: number;
  outliers: number;
}

/** Percentil por interpolação linear (mesmo método usado nas auditorias de RQ02/RQ03). */
export function percentile(sortedValues: number[], position: number): number {
  const index = (sortedValues.length - 1) * position;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  return lower === upper
    ? sortedValues[lower]
    : sortedValues[lower] + (sortedValues[upper] - sortedValues[lower]) * (index - lower);
}

/** Resumo estatístico com detecção de outliers pelo critério de Tukey (Q1 - 1,5×IQR / Q3 + 1,5×IQR). */
export function summarize(values: number[]): MetricSummary {
  const clean = values.filter((value) => Number.isFinite(value));
  if (clean.length === 0) {
    throw new Error('Não é possível resumir uma lista vazia de valores.');
  }

  const sorted = [...clean].sort((a, b) => a - b);
  const q1 = percentile(sorted, 0.25);
  const q3 = percentile(sorted, 0.75);
  const iqr = q3 - q1;
  const lowerFence = q1 - 1.5 * iqr;
  const upperFence = q3 + 1.5 * iqr;

  return {
    count: clean.length,
    minimum: sorted[0],
    q1,
    median: percentile(sorted, 0.5),
    mean: clean.reduce((sum, value) => sum + value, 0) / clean.length,
    q3,
    maximum: sorted[sorted.length - 1],
    iqr,
    lowerFence,
    upperFence,
    outliers: clean.filter((value) => value < lowerFence || value > upperFence).length,
  };
}

export function round(value: number, decimals = 2): number {
  const factor = 10 ** decimals;
  return Math.round(value * factor) / factor;
}

/** Arredonda todos os campos numéricos de um MetricSummary, para exibição em relatórios/JSON. */
export function roundSummary(summary: MetricSummary, decimals = 2): MetricSummary {
  return {
    ...summary,
    minimum: round(summary.minimum, decimals),
    q1: round(summary.q1, decimals),
    median: round(summary.median, decimals),
    mean: round(summary.mean, decimals),
    q3: round(summary.q3, decimals),
    maximum: round(summary.maximum, decimals),
    iqr: round(summary.iqr, decimals),
    lowerFence: round(summary.lowerFence, decimals),
    upperFence: round(summary.upperFence, decimals),
  };
}

export interface Bucket {
  faixa: string;
  contagem: number;
  percentual: number;
}

/**
 * Distribui valores em faixas cumulativas: cada `edge[i]` é o limite superior
 * (inclusive) da faixa `labels[i]`; use `Infinity` na última faixa para
 * capturar o restante. Ex.: edges=[1,2,Infinity], labels=['<=1','1-2','2+'].
 */
export function distribution(values: number[], edges: number[], labels: string[]): Bucket[] {
  if (edges.length !== labels.length) {
    throw new Error('distribution: edges e labels devem ter o mesmo tamanho.');
  }
  const clean = values.filter((value) => Number.isFinite(value));
  const counts = new Array(labels.length).fill(0);
  for (const value of clean) {
    const bucketIndex = edges.findIndex((edge) => value <= edge);
    counts[bucketIndex === -1 ? counts.length - 1 : bucketIndex]++;
  }
  return labels.map((faixa, index) => ({
    faixa,
    contagem: counts[index],
    percentual: clean.length === 0 ? 0 : round((counts[index] / clean.length) * 100, 1),
  }));
}
