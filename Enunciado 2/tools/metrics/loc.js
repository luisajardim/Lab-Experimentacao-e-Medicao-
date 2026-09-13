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
      if (trimmed === '') break;

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

    if (hasCode) codeLines++;
    else if (hasComment) commentLines++;
    else blankLines++;
  }

  return {
    total: lines.length,
    code: codeLines,
    blank: blankLines,
    comments: commentLines,
  };
}

module.exports = { calcLOC };