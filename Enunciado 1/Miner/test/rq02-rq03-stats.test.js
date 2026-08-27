const test = require('node:test');
const assert = require('node:assert/strict');
const { buildRq02Rq03ReportData, renderRq02Rq03Report } = require('../dist/scripts/engajamento-rq02-rq03');

test('calcula medianas e distribuições de PRs aceitas e releases', () => {
  const rows = [
    { nome: 'repo-a', total_pr_aceitas: 100, total_releases: 0 },
    { nome: 'repo-b', total_pr_aceitas: 200, total_releases: 10 },
    { nome: 'repo-c', total_pr_aceitas: 300, total_releases: 50 },
    { nome: 'repo-d', total_pr_aceitas: 400, total_releases: 200 },
    { nome: 'repo-e', total_pr_aceitas: 500, total_releases: 300 },
  ];

  const data = buildRq02Rq03ReportData(rows);
  assert.equal(data.totalRepositorios, 5);
  assert.equal(data.prsAceitas.resumo.median, 300);
  assert.equal(data.releases.resumo.median, 50);
  assert.equal(data.prsAceitas.faixas[0].faixa, 'até 100');
  assert.match(renderRq02Rq03Report(data, 'sample.csv'), /RQ02/);
});
