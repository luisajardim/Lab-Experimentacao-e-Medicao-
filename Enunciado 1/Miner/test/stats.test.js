const test = require('node:test');
const assert = require('node:assert/strict');
const { summarize, distribution, percentile, round } = require('../dist/core/stats');

test('percentile interpola linearmente entre dois pontos', () => {
  assert.equal(percentile([1, 2, 3, 4], 0.5), 2.5);
  assert.equal(percentile([1, 2, 3, 4, 5], 0.5), 3);
});

test('summarize calcula quartis e média corretamente', () => {
  const summary = summarize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
  assert.equal(summary.count, 10);
  assert.equal(summary.median, 5.5);
  assert.equal(summary.q1, 3.25);
  assert.equal(summary.q3, 7.75);
  assert.equal(summary.mean, 5.5);
});

test('summarize detecta outlier acima do limite superior de Tukey', () => {
  const summary = summarize([1, 1, 1, 1, 1, 1, 1, 1, 1, 1000]);
  assert.equal(summary.outliers, 1);
});

test('summarize ignora valores não finitos (NaN/Infinity)', () => {
  const summary = summarize([1, 2, 3, NaN, Infinity]);
  assert.equal(summary.count, 3);
});

test('summarize lança erro para lista vazia', () => {
  assert.throws(() => summarize([]), /lista vazia/);
});

test('distribution agrupa valores em faixas cumulativas', () => {
  const buckets = distribution([0.5, 1, 1.5, 2, 10], [1, 2, Infinity], ['<=1', '1-2', '2+']);
  assert.deepEqual(buckets, [
    { faixa: '<=1', contagem: 2, percentual: 40 },
    { faixa: '1-2', contagem: 2, percentual: 40 },
    { faixa: '2+', contagem: 1, percentual: 20 },
  ]);
});

test('distribution lança erro se edges e labels tiverem tamanhos diferentes', () => {
  assert.throws(() => distribution([1], [1, 2], ['a']), /mesmo tamanho/);
});

test('round arredonda para o número de casas decimais informado', () => {
  assert.equal(round(1.23456, 2), 1.23);
  assert.equal(round(2.5, 0), 3);
});
