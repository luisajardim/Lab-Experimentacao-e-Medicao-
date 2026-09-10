#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const escomplex = require('escomplex');

function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = args[i + 1];
    if (next && !next.startsWith('--')) {
      parsed[key] = next;
      i++;
    } else {
      parsed[key] = true;
    }
  }
  return parsed;
}

const cli = parseArgs();

if (!cli.path) {
  console.error('Uso: node tools/metrics-runner.js --path <caminho-do-trial>');
  process.exit(1);
}

const trialPath = path.resolve(cli.path);
const indexFile = path.join(trialPath, 'index.js');

if (!fs.existsSync(indexFile)) {
  console.error(`Arquivo não encontrado: ${indexFile}`);
  process.exit(1);
}

function calcLOC(source) {
  const noComments = source
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/\/\/.*/g, '');
  return noComments.split('\n').filter(line => line.trim().length > 0).length;
}

function calcCyclomatic(source) {
  try {
    const report = escomplex.analyse(source);
    return report.aggregate.cyclomatic;
  } catch {
    return null;
  }
}

function calcDuplication(dirPath) {
  const tempDir = path.join(dirPath, '.jscpd-temp');
  try {
    execSync(
      `npx jscpd "${dirPath}" --reporters json --output "${tempDir}" --ignore "**/*.test.js" --min-lines 3 --silent`,
      { stdio: 'pipe' }
    );
    const reportFile = path.join(tempDir, 'jscpd-report.json');
    if (!fs.existsSync(reportFile)) {
      return { duplicated_lines: 0, duplication_percentage: 0.0 };
    }
    const report = JSON.parse(fs.readFileSync(reportFile, 'utf8'));
    const stats = report.statistics?.total ?? {};
    return {
      duplicated_lines: stats.duplicatedLines ?? 0,
      duplication_percentage: parseFloat((stats.percentage ?? 0).toFixed(2)),
    };
  } catch {
    return { duplicated_lines: 0, duplication_percentage: 0.0 };
  } finally {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  }
}

function buildTrialId(resolvedPath) {
  const parts = resolvedPath.replace(/\\/g, '/').split('/');
  const trialsIdx = parts.indexOf('trials');
  if (trialsIdx !== -1 && parts.length > trialsIdx + 2) {
    return `${parts[trialsIdx + 1]}-${parts[trialsIdx + 2]}`;
  }
  return path.basename(resolvedPath);
}

const source = fs.readFileSync(indexFile, 'utf8');

const loc = calcLOC(source);
const cyclomatic = calcCyclomatic(source);
const { duplicated_lines, duplication_percentage } = calcDuplication(trialPath);
const trial_id = buildTrialId(trialPath);

const output = {
  trial_id,
  metrics: {
    loc,
    cyclomatic_complexity: cyclomatic,
    duplicated_lines,
    duplication_percentage,
  },
};

const outputFile = path.join(trialPath, 'metrics.json');
fs.writeFileSync(outputFile, JSON.stringify(output, null, 2) + '\n', 'utf8');

console.log(`✅ Métricas calculadas para: ${trial_id}`);
console.log(`   LOC:                    ${loc}`);
console.log(`   Complexidade Ciclomática: ${cyclomatic}`);
console.log(`   Linhas duplicadas:       ${duplicated_lines}`);
console.log(`   Duplicação (%):          ${duplication_percentage}%`);
console.log(`💾 Salvo em: ${outputFile}`);
