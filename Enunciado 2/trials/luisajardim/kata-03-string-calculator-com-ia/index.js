function add(numbers) {
  if (numbers === "") return 0;

  let delimiter = /,|\n/;
  let body = numbers;

  if (numbers.startsWith("//")) {
    const newlineIndex = numbers.indexOf("\n");
    const customDelimiter = numbers.slice(2, newlineIndex);
    delimiter = new RegExp(customDelimiter.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    body = numbers.slice(newlineIndex + 1);
  }

  const nums = body
    .split(delimiter)
    .map((value) => value.trim())
    .filter((value) => value.length > 0)
    .map(Number);

  const negatives = nums.filter((value) => value < 0);
  if (negatives.length > 0) {
    throw new Error(`negatives not allowed: ${negatives.join(", ")}`);
  }

  return nums.reduce((sum, value) => sum + value, 0);
}

module.exports = { add };
