function paginate(items, pageSize, pageNumber) {
  return {
    data: [],
    totalPages: 0,
    hasNext: false,
    hasPrev: false,
  };
}

module.exports = { paginate };
