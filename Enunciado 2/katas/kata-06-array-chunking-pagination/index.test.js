const { paginate } = require("./index");

describe("paginate", () => {
  describe("caso básico", () => {
    test("retorna a primeira página com metadados corretos", () => {
      expect(paginate(["A", "B", "C", "D"], 2, 1)).toEqual({
        data: ["A", "B"],
        totalPages: 2,
        hasNext: true,
        hasPrev: false,
      });
    });

    test("retorna a segunda página com metadados corretos", () => {
      expect(paginate(["A", "B", "C", "D"], 2, 2)).toEqual({
        data: ["C", "D"],
        totalPages: 2,
        hasNext: false,
        hasPrev: true,
      });
    });
  });

  describe("chunking de arrays", () => {
    test("divide um array em páginas de tamanho 3", () => {
      expect(paginate([1, 2, 3, 4, 5, 6, 7], 3, 2)).toEqual({
        data: [4, 5, 6],
        totalPages: 3,
        hasNext: true,
        hasPrev: true,
      });
    });

    test("retorna a última fatia parcial do array", () => {
      expect(paginate([1, 2, 3, 4, 5], 2, 3)).toEqual({
        data: [5],
        totalPages: 3,
        hasNext: false,
        hasPrev: true,
      });
    });
  });

  describe("limites da paginação", () => {
    test("retorna data vazia para página fora do intervalo", () => {
      expect(paginate(["A", "B", "C"], 2, 3)).toEqual({
        data: [],
        totalPages: 2,
        hasNext: false,
        hasPrev: true,
      });
    });

    test("retorna data vazia para array vazio", () => {
      expect(paginate([], 2, 1)).toEqual({
        data: [],
        totalPages: 0,
        hasNext: false,
        hasPrev: false,
      });
    });
  });

  describe("validação de entrada", () => {
    test("lança erro para pageSize igual a zero", () => {
      expect(() => paginate(["A"], 0, 1)).toThrow();
    });

    test("lança erro para pageNumber igual a zero", () => {
      expect(() => paginate(["A"], 1, 0)).toThrow();
    });

    test("lança erro para pageSize não inteiro", () => {
      expect(() => paginate(["A"], 1.5, 1)).toThrow();
    });

    test("lança erro para valores inválidos", () => {
      expect(() => paginate("A", 1, 1)).toThrow();
    });
  });
});
