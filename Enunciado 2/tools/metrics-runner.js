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

    if (!arg.startsWith('--')) {
      continue;
    }

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
  console.error(
    'Uso: node tools/metrics-runner.js --path <caminho-do-trial>'
  );
  process.exit(1);
}

const trialPath = path.resolve(cli.path);
const indexFile = path.join(trialPath, 'index.js');

if (!fs.existsSync(indexFile)) {
  console.error(`Arquivo não encontrado: ${indexFile}`);
  process.exit(1);
}

function calcLOC(source) {
  const lines = source.split(/\r?\n/);

  let codeLines = 0;
  let blankLines = 0;
  let commentLines = 0;
  let inBlockComment = false;

  for (const line of lines) {
    let remaining = line;
    let hasCode = false;
    let hasComment = false;

    while (remaining.length > 0) {
      if (inBlockComment) {
        hasComment = true;

        const end = remaining.indexOf('*/');

        if (end === -1) {
          remaining = '';
          break;
        }

        remaining = remaining.slice(end + 2);
        inBlockComment = false;
        continue;
      }

      const trimmed = remaining.trim();

      if (trimmed === '') {
        break;
      }

      if (trimmed.startsWith('//')) {
        hasComment = true;
        break;
      }

      if (trimmed.startsWith('/*')) {
        hasComment = true;

        const end = remaining.indexOf('*/', 2);

        if (end === -1) {
          inBlockComment = true;
          remaining = '';
          break;
        }

        remaining = remaining.slice(end + 2);
        continue;
      }

      hasCode = true;
      break;
    }

    if (hasCode) {
      codeLines++;
    } else if (hasComment) {
      commentLines++;
    } else {
      blankLines++;
    }
  }

  return {
    total: lines.length,
    code: codeLines,
    blank: blankLines,
    comments: commentLines,
  };
}

function calcCyclomatic(source) {
  try {
    const report = escomplex.analyse(source);

    if (!report || !Array.isArray(report.functions)) {
      throw new Error(
        'Formato inesperado no relatório do escomplex: functions não encontrado'
      );
    }

    const functions = report.functions.filter(
      (fn) =>
        fn &&
        typeof fn.cyclomatic === 'number' &&
        fn.line !== 0
    );

    if (functions.length === 0) {
      return {
        average: 0,
        function_count: 0,
      };
    }

    const total = functions.reduce(
      (sum, fn) => sum + fn.cyclomatic,
      0
    );

    const average = total / functions.length;

    return {
      average: Number(average.toFixed(2)),
      function_count: functions.length,
    };
  } catch (error) {
    throw new Error(
      `Falha ao calcular complexidade ciclomática: ${error.message}`
    );
  }
}

function calcDuplication(indexFile, dirPath) {
  const tempDir = path.join(dirPath, '.jscpd-temp');

  try {
    execSync(
      [
        'npx --no-install jscpd',
        `"${indexFile}"`,
        '--reporters json',
        `--output "${tempDir}"`,
        '--ignore "**/*.test.js,**/metrics.json,**/.jscpd-temp/**"',
        '--min-lines 3',
        '--min-tokens 20',
        '--silent',
      ].join(' '),
      { stdio: 'pipe' }
    );

    const reportFile = path.join(
      tempDir,
      'jscpd-report.json'
    );

    if (!fs.existsSync(reportFile)) {
      throw new Error(
        `Relatório do jscpd não encontrado: ${reportFile}`
      );
    }

    const report = JSON.parse(
      fs.readFileSync(reportFile, 'utf8')
    );

    const stats = report.statistics?.total;

    if (!stats) {
      throw new Error(
        'Estatísticas do jscpd não encontradas no relatório.'
      );
    }

    const totalLines = Number(stats.lines);
    const duplicatedLines = Number(stats.duplicatedLines);

    if (!Number.isFinite(totalLines)) {
      throw new Error(
        'Número de linhas analisadas pelo jscpd não encontrado.'
      );
    }

    if (!Number.isFinite(duplicatedLines)) {
      throw new Error(
        'Número de linhas duplicadas pelo jscpd não encontrado.'
      );
    }

    const duplicationPercentage =
      totalLines > 0
        ? Number(
          ((duplicatedLines / totalLines) * 100).toFixed(2)
        )
        : 0;

    return {
      duplicated_lines: duplicatedLines,
      duplication_total_lines: totalLines,
      duplication_percentage: duplicationPercentage,
    };
  } catch (error) {
    throw new Error(
      `Falha ao calcular duplicação com jscpd: ${error.message}`
    );
  } finally {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, {
        recursive: true,
        force: true,
      });
    }
  }
}

function buildTrialId(resolvedPath) {
  const parts = resolvedPath
    .replace(/\\/g, '/')
    .split('/');

  const trialsIdx = parts.indexOf('trials');

  if (trialsIdx !== -1 && parts.length > trialsIdx + 2) {
    return `${parts[trialsIdx + 1]}-${parts[trialsIdx + 2]}`;
  }

  return path.basename(resolvedPath);
}

function main() {
  const source = fs.readFileSync(indexFile, 'utf8');

  const loc = calcLOC(source);
  const cyclomatic = calcCyclomatic(source);
  const duplication = calcDuplication(indexFile, trialPath);
  const trial_id = buildTrialId(trialPath);

  const output = {
    trial_id,
    metrics: {
      loc: loc.code,
      cyclomatic_complexity: cyclomatic.average,
      function_count: cyclomatic.function_count,
      duplicated_lines: duplication.duplicated_lines,
      duplication_total_lines: duplication.duplication_total_lines,
      duplication_percentage: duplication.duplication_percentage,
    },
  };

  const outputFile = path.join(
    trialPath,
    'metrics.json'
  );

  fs.writeFileSync(
    outputFile,
    JSON.stringify(output, null, 2) + '\n',
    'utf8'
  );

  console.log(`Métricas calculadas para: ${trial_id}`);
  console.log(`LOC: ${loc.code}`);
  console.log(
    `Complexidade Ciclomática Média: ${cyclomatic.average}`
  );
  console.log(
    `Funções analisadas: ${cyclomatic.function_count}`
  );
  console.log(
    `Linhas duplicadas: ${duplication.duplicated_lines}`
  );
  console.log(
    `Linhas analisadas pelo jscpd: ${duplication.duplication_total_lines}`
  );
  console.log(
    `Duplicação (%): ${duplication.duplication_percentage}%`
  );
  console.log(`Salvo em: ${outputFile}`);
}

try {
  main();
} catch (error) {
  console.error(`Erro: ${error.message}`);
  process.exit(1);
}
