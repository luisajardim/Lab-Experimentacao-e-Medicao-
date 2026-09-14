function add(numbers) {
  if (numbers === undefined || numbers === null) {
    throw new Error('A entrada deve ser uma string.');
  }

  if (numbers.length === 0) return 0;

  let input = numbers;
  let delimiter = ',';

  if (input.startsWith('//')) {
    const newlineIndex = input.indexOf('\n');
    if (newlineIndex === -1) {
      throw new Error('Delimitador customizado mal formatado.');
    }
    delimiter = input.slice(2, newlineIndex);
    input = input.slice(newlineIndex + 1);
  }

  const normalized = input.split('\n').join(delimiter);
  const tokens = normalized.split(delimiter).filter(token => token !== '');
  const nums = tokens.map(token => Number(token));

  const negatives = nums.filter(num => num < 0);
  if (negatives.length > 0) {
    throw new Error(`${negatives.join(',')}`);
  }

  return nums.reduce((sum, num) => sum + num, 0);
}

module.exports = { add };
