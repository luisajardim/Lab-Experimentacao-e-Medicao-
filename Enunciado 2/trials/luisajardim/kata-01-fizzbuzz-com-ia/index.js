function fizzbuzz(n) {
  if (typeof n !== "number" || !Number.isInteger(n) || n < 0) {
    throw new TypeError("n must be a non-negative integer");
  }

  const result = [];
  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) result.push("FizzBuzz");
    else if (i % 3 === 0) result.push("Fizz");
    else if (i % 5 === 0) result.push("Buzz");
    else result.push(String(i));
  }
  return result;
}

module.exports = { fizzbuzz };
