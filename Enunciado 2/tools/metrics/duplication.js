const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

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

    const reportFile = path.join(tempDir, 'jscpd-report.json');
    if (!fs.existsSync(reportFile)) {
      throw new Error(`Relatório do jscpd não encontrado: ${reportFile}`);
    }

    const report = JSON.parse(fs.readFileSync(reportFile, 'utf8'));
    const stats = report.statistics?.total;

    if (!stats) {
      throw new Error('Estatísticas do jscpd não encontradas no relatório.');
    }

    const totalLines = Number(stats.lines);
    const duplicatedLines = Number(stats.duplicatedLines);

    const duplicationPercentage =
      totalLines > 0
        ? Number(((duplicatedLines / totalLines) * 100).toFixed(2))
        : 0;

    return {
      duplicated_lines: duplicatedLines,
      duplication_total_lines: totalLines,
      duplication_percentage: duplicationPercentage,
    };
  } catch (error) {
    throw new Error(`Falha ao calcular duplicação com jscpd: ${error.message}`);
  } finally {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  }
}

module.exports = { calcDuplication };