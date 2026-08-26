const test = require('node:test');
const assert = require('node:assert/strict');
const { buildMaturityReportData, renderMaturityReport } = require('../dist/scripts/maturidade-rq01-rq04');

function makeRow(overrides) {
  return { nome: 'org/repo', idade_anos: 5, dias_desde_ultima_atualizacao: 10, ...overrides };
}

test('calcula resumo e faixas etárias para RQ01', () => {
  const rows = [
    makeRow({ idade_anos: 0.5 }),
    makeRow({ idade_anos: 1.5 }),
    makeRow({ idade_anos: 6 }),
    makeRow({ idade_anos: 12 }),
    makeRow({ idade_anos: 16 }),
  ];
  const data = buildMaturityReportData(rows);
  assert.equal(data.totalRepositorios, 5);
  assert.equal(data.idadeAnos.resumo.count, 5);

  const faixas = Object.fromEntries(data.idadeAnos.faixas.map((b) => [b.faixa, b.contagem]));
  assert.equal(faixas['até 1 ano'], 1);
  assert.equal(faixas['1-2 anos'], 1);
  assert.equal(faixas['5-10 anos'], 1);
  assert.equal(faixas['10-15 anos'], 1);
  assert.equal(faixas['15+ anos'], 1);
});

test('identifica os maiores outliers nomeados de dias sem atualização', () => {
  const rows = [
    ...Array.from({ length: 9 }, () => makeRow({ dias_desde_ultima_atualizacao: 1 })),
    makeRow({ nome: 'org/abandonado', dias_desde_ultima_atualizacao: 5000 }),
  ];
  const data = buildMaturityReportData(rows);
  assert.equal(data.diasDesdeUltimaAtualizacao.resumo.outliers, 1);
  assert.equal(data.diasDesdeUltimaAtualizacao.maioresOutliers[0].nome, 'org/abandonado');
  assert.equal(data.diasDesdeUltimaAtualizacao.maioresOutliers[0].valor, 5000);
});

test('validação sinaliza valores ausentes e negativos', () => {
  const rows = [
    makeRow({ idade_anos: '' }),
    makeRow({ dias_desde_ultima_atualizacao: -3 }),
    makeRow({}),
  ];
  const data = buildMaturityReportData(rows);
  assert.equal(data.validacao.ausentesIdade, 1);
  assert.equal(data.validacao.negativosDias, 1);
});

test('lança erro para dataset vazio', () => {
  assert.throws(() => buildMaturityReportData([]), /Dataset vazio/);
});

test('renderMaturityReport gera markdown com as seções esperadas', () => {
  const rows = Array.from({ length: 5 }, (_, i) => makeRow({ idade_anos: i + 1, dias_desde_ultima_atualizacao: i }));
  const data = buildMaturityReportData(rows);
  const markdown = renderMaturityReport(data, 'data/fixture.csv');
  assert.match(markdown, /RQ01 — Idade do repositório/);
  assert.match(markdown, /RQ04 — Dias desde a última atualização/);
  assert.match(markdown, /Validação de consistência/);
  assert.match(markdown, /data\/fixture\.csv/);
});
