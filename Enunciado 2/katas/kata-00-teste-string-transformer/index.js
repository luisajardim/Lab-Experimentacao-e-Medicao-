function transformString(value) {
  if (typeof value !== "string") {
    throw new TypeError("value must be a string");
  }

  return value
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map((word) => [...word].reverse().join(""))
    .join(" ");
}

module.exports = { transformString };