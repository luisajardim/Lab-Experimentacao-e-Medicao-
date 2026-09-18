const escomplex = require('escomplex');
const esprima = require('esprima');

function getClassMethodReports(source) {
  const ast = esprima.parse(source, { loc: true, range: true });
  const reports = [];

  function visit(node) {
    if (!node || typeof node !== 'object') return;

    if (node.type === 'MethodDefinition' && node.value && node.value.body) {
      const params = node.value.params
        .map((param) => source.slice(param.range[0], param.range[1]))
        .join(', ');
      const body = source.slice(
        node.value.body.range[0],
        node.value.body.range[1]
      );
      const name = node.key.name || node.key.value || 'class method';
      const methodSource = `function ${name}(${params}) ${body}`;
      const report = escomplex.analyse(methodSource);

      reports.push(...report.functions);
      return;
    }

    Object.keys(node).forEach((key) => {
      if (key !== 'loc' && key !== 'range') visit(node[key]);
    });
  }

  visit(ast);
  return reports;
}

function calcComplexityAndHalstead(source) {
  try {
    const report = escomplex.analyse(source);

    if (!report || !Array.isArray(report.functions)) {
      throw new Error('Formato inesperado no relatório do escomplex');
    }

    let functions = report.functions.filter(
      (fn) => fn && typeof fn.cyclomatic === 'number' && fn.line !== 0
    );

    // escomplex 2 alpha does not register methods declared inside classes.
    const classMethods = getClassMethodReports(source).filter(
        (fn) => fn && typeof fn.cyclomatic === 'number' && fn.line !== 0
    );
    functions = functions.concat(classMethods);

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