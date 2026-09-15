function paginate(items, pageSize, pageNumber) {
  if (!Array.isArray(items)) throw new Error("items must be an array");
  if (!Number.isInteger(pageSize) || pageSize <= 0) throw new Error("pageSize must be > 0");
  if (!Number.isInteger(pageNumber) || pageNumber <= 0) throw new Error("pageNumber must be > 0");

  const totalPages = Math.ceil(items.length / pageSize);
  const data = items.slice((pageNumber - 1) * pageSize, pageNumber * pageSize);
  return {
    data,
    totalPages,
    hasNext: pageNumber < totalPages,
    hasPrev: pageNumber > 1 && items.length > 0
  };
}
module.exports = { paginate };
