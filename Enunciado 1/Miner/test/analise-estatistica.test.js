const test = require('node:test');
const assert = require('node:assert/strict');
const { buildMetricsSummary } = require('../dist/scripts/analise-estatistica');

function makeRow(overrides) {
  return {
    nome: 'org/repo',
    linguagem: 'TypeScript',
    idade_anos: 5,
    dias_desde_ultima_atualizacao: 1,
    total_pr_aceitas: 10,
    total_releases: 1,
    total_issues: 10,
    total_issues_fechadas: 8,
    razao_issues_fechadas: 0.8,
    ...overrides,
  };
}

test('calcula mediana e quartis corretamente para um conjunto conhecido', () => {
  // idade_anos: 1,2,3,4,5,6,7,8,9,10 -> mediana 5.5, Q1 3.25, Q3 7.75
  const rows = Array.from({ length: 10 }, (_, i) => makeRow({ idade_anos: i + 1 }));
  const summary = buildMetricsSummary(rows);

  assert.equal(summary.totalRepositorios, 10);
  assert.equal(summary.metricas.idade_anos.median, 5.5);
  assert.equal(summary.metricas.idade_anos.q1, 3.25);
  assert.equal(summary.metricas.idade_anos.q3, 7.75);
  assert.equal(summary.metricas.idade_anos.minimum, 1);
  assert.equal(summary.metricas.idade_anos.maximum, 10);
});

test('marca como outlier um valor muito acima do limite superior de Tukey', () => {
  const rows = [
    ...Array.from({ length: 9 }, () => makeRow({ dias_desde_ultima_atualizacao: 1 })),
    makeRow({ dias_desde_ultima_atualizacao: 10000 }),
  ];
  const summary = buildMetricsSummary(rows);
  assert.equal(summary.metricas.dias_desde_ultima_atualizacao.outliers, 1);
});

test('gera contagem de linguagens (RQ05) ordenada por popularidade', () => {
  const rows = [
    makeRow({ linguagem: 'Python' }),
    makeRow({ linguagem: 'Python' }),
    makeRow({ linguagem: 'TypeScript' }),
  ];
  const summary = buildMetricsSummary(rows);
  assert.deepEqual(summary.rq05_linguagens[0], { linguagem: 'Python', contagem: 2, percentual: 66.7 });
});

test('trata linguagem ausente como N/A', () => {
  const rows = [makeRow({ linguagem: '' }), makeRow({ linguagem: '' })];
  const summary = buildMetricsSummary(rows);
  assert.deepEqual(summary.rq05_linguagens[0], { linguagem: 'N/A', contagem: 2, percentual: 100 });
});

test('cruza métricas por linguagem para RQ07 usando a mediana', () => {
  const rows = [
    makeRow({ linguagem: 'Python', total_pr_aceitas: 10 }),
    makeRow({ linguagem: 'Python', total_pr_aceitas: 20 }),
  ];
  const summary = buildMetricsSummary(rows);
  const python = summary.rq07_cruzamentoPorLinguagem.find((entry) => entry.linguagem === 'Python');
  assert.equal(python.repositorios, 2);
  assert.equal(python.pr_aceitas_mediana, 15);
});

test('lança erro para dataset vazio', () => {
  assert.throws(() => buildMetricsSummary([]), /Dataset vazio/);
});
