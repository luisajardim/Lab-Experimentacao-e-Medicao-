function paginate(items, pageSize, pageNumber) {
    if (!Array.isArray(items) || !Number.isInteger(pageSize) || pageSize <= 0 ||
        !Number.isInteger(pageNumber) || pageNumber <= 0) {
        throw new Error('Parâmetros inválidos');
    }

    const pages = [];
    for (let start = 0; start < items.length; start += pageSize) {
        pages.push(items.slice(start, start + pageSize));
    }

    return {
        data: pages[pageNumber - 1] || [],
        totalPages: pages.length,
        hasNext: pageNumber < pages.length,
        hasPrev: pageNumber > 1 && pages.length > 0,
    };
}

module.exports = { paginate };
