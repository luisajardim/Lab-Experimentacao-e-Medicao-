const VALUES = [
  [1000, "M"],
  [900, "CM"],
  [500, "D"],
  [400, "CD"],
  [100, "C"],
  [90, "XC"],
  [50, "L"],
  [40, "XL"],
  [10, "X"],
  [9, "IX"],
  [5, "V"],
  [4, "IV"],
  [1, "I"],
];

function toRoman(num) {
  if (typeof num !== "number" || !Number.isInteger(num) || num < 1 || num > 3999) {
    throw new RangeError("num must be an integer between 1 and 3999");
  }

  let remaining = num;
  let result = "";
  for (const [value, symbol] of VALUES) {
    while (remaining >= value) {
      result += symbol;
      remaining -= value;
    }
  }
  return result;
}

module.exports = { toRoman };
