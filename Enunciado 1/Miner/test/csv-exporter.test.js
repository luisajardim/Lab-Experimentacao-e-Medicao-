const test = require('node:test');
const assert = require('node:assert/strict');
const { buildCsvRows } = require('../dist/exporters/csv-exporter');

test('normaliza ausências e números para valores seguros no CSV', () => {
  const rows = buildCsvRows([{
    nameWithOwner: 'org/repo',
    pullRequests: { totalCount: null },
    releases: undefined,
    primaryLanguage: null,
  }], [
    { name: 'nome', jsonPath: '$.nameWithOwner', type: 'string', default: '' },
    { name: 'total_pr_aceitas', jsonPath: '$.pullRequests.totalCount', type: 'integer', default: 0 },
    { name: 'total_releases', jsonPath: '$.releases.totalCount', type: 'integer', default: 0 },
    { name: 'linguagem', jsonPath: '$.primaryLanguage.name', type: 'string', default: 'N/A' },
  ], new Date('2026-01-01T00:00:00.000Z'));

  assert.deepEqual(rows, [{
    nome: 'org/repo',
    total_pr_aceitas: 0,
    total_releases: 0,
    linguagem: 'N/A',
  }]);
});

test('converte contagens para inteiros não negativos', () => {
  const rows = buildCsvRows([{ value: 12.8 }, { value: -1 }, { value: 'invalid' }], [
    { name: 'contagem', jsonPath: '$.value', type: 'integer', default: 0 },
  ], new Date());

  assert.deepEqual(rows, [{ contagem: 12 }, { contagem: 0 }, { contagem: 0 }]);
});

test('calcula a razão de issues fechadas a partir do registro', () => {
  const rows = buildCsvRows([{
    totalIssues: { totalCount: 8 },
    closedIssues: { totalCount: 6 },
  }], [{ name: 'razao', transform: 'closedIssuesRatio', type: 'number', default: 0 }], new Date());

  assert.deepEqual(rows, [{ razao: 0.75 }]);
});
