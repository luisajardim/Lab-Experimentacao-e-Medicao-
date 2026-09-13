#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const { calcLOC } = require('./metrics/loc');
const { calcComplexityAndHalstead } = require('./metrics/complexity');
const { calcDuplication } = require('./metrics/duplication');
const { parseArgs } = require('./utils');

function buildTrialId(resolvedPath) {
  const parts = resolvedPath.replace(/\\/g, '/').split('/');
  const trialsIdx = parts.indexOf('trials');

  if (trialsIdx !== -1 && parts.length > trialsIdx + 2) {
    return `${parts[trialsIdx + 1]}-${parts[trialsIdx + 2]}`;
  }

  return path.basename(resolvedPath);
}

const cli = parseArgs();

if (!cli.path) {
  console.error('Uso: npm run metrics -- --path <caminho-do-trial>');
  process.exit(1);
}

const trialPath = path.resolve(cli.path);
const indexFile = path.join(trialPath, 'index.js');

if (!fs.existsSync(indexFile)) {
  console.error(`❌ Arquivo não encontrado: ${indexFile}`);
  process.exit(1);
}

function main() {
  const source = fs.readFileSync(indexFile, 'utf8');

  // Execução dos módulos
  const loc = calcLOC(source);
  const { cyclomatic, halstead } = calcComplexityAndHalstead(source);
  const duplication = calcDuplication(indexFile, trialPath);
  const trial_id = buildTrialId(trialPath);

  // Estrutura final do json
  const output = {
    trial_id,
    metrics: {
      loc: loc.code,
      cyclomatic_complexity: cyclomatic.average,
      function_count: cyclomatic.function_count,
      halstead: halstead,
      duplication: {
        total_lines: duplication.duplication_total_lines,
        duplicated_lines: duplication.duplicated_lines,
        percentage: duplication.duplication_percentage,
      },
    },
  };

  const outputFile = path.join(trialPath, 'metrics.json');

  fs.writeFileSync(
    outputFile,
    JSON.stringify(output, null, 2) + '\n',
    'utf8'
  );

  console.log(`\n========================================`);
  console.log(`📊 Métricas calculadas para: ${trial_id}`);
  console.log(`========================================`);
  console.log(`LoC (Somente código): ${loc.code}`);
  console.log(`Complexidade Ciclomática Média: ${cyclomatic.average}`);
  console.log(`Funções analisadas: ${cyclomatic.function_count}`);
  console.log(`Volume de Halstead: ${halstead.volume}`);
  console.log(`Dificuldade de Halstead: ${halstead.difficulty}`);
  console.log(`Esforço de Halstead: ${halstead.effort}`);
  console.log(`Duplicação (%): ${duplication.duplication_percentage}%`);
  console.log(`========================================`);
  console.log(`📂 Salvo em: ${outputFile}\n`);
}

try {
  main();
} catch (error) {
  console.error(`❌ Erro: ${error.message}`);
  process.exit(1);
}