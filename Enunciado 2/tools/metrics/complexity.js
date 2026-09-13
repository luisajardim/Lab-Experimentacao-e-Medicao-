const escomplex = require('escomplex');

function calcComplexityAndHalstead(source) {
  try {
    const report = escomplex.analyse(source);

    if (!report || !Array.isArray(report.functions)) {
      throw new Error('Formato inesperado no relatório do escomplex');
    }

    const functions = report.functions.filter(
      (fn) => fn && typeof fn.cyclomatic === 'number' && fn.line !== 0
    );

    // 1. Complexidade Ciclomática
    const totalCyclomatic = functions.reduce((sum, fn) => sum + fn.cyclomatic, 0);
    const cyclomaticAvg = functions.length > 0 ? totalCyclomatic / functions.length : 0;

    // 2. Halstead (extraído diretamente do report aggregate)
    const halstead = report.aggregate?.halstead || { volume: 0, difficulty: 0 };

    return {
      cyclomatic: {
        average: Number(cyclomaticAvg.toFixed(2)),
        function_count: functions.length,
      },
      halstead: {
        volume: Number((halstead.volume || 0).toFixed(2)),
        difficulty: Number((halstead.difficulty || 0).toFixed(2)),
        effort: Number((halstead.effort || 0).toFixed(2)),
      },
    };
  } catch (error) {
    throw new Error(`Falha ao calcular métricas AST (escomplex): ${error.message}`);
  }
}

module.exports = { calcComplexityAndHalstead };