const test = require('node:test');
const assert = require('node:assert/strict');
const { parseCsvToJson } = require('../dist/scripts/csv-to-json');

test('converte CSV com aspas, quebras de linha e tipos escalares seguros', () => {
  const rows = parseCsvToJson('\uFEFFnome,valor,ativo,descricao\r\n"org, repo",12.5,true,"linha 1\nlinha 2"\r\n');
  assert.deepEqual(rows, [{ nome: 'org, repo', valor: 12.5, ativo: true, descricao: 'linha 1\nlinha 2' }]);
});

test('preserva códigos com zero à esquerda e permite desabilitar inferência', () => {
  assert.deepEqual(parseCsvToJson('codigo,valor\n001,10\n', { inferTypes: false }), [{ codigo: '001', valor: '10' }]);
  assert.deepEqual(parseCsvToJson('codigo,valor\n001,10\n'), [{ codigo: '001', valor: 10 }]);
});
