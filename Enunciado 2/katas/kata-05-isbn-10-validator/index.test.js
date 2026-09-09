const { isValidISBN10 } = require("./index");

describe("isValidISBN10", () => {
  describe("casos válidos", () => {
    test("valida um ISBN-10 conhecido", () => {
      expect(isValidISBN10("0471958697")).toBe(true);
    });

    test("valida outro ISBN-10 conhecido", () => {
      expect(isValidISBN10("0306406152")).toBe(true);
    });

    test("aceita X como último caractere", () => {
      expect(isValidISBN10("030640615X")).toBe(true);
    });
  });

  describe("casos inválidos", () => {
    test("retorna false para soma não divisível por 11", () => {
      expect(isValidISBN10("047195869X")).toBe(false);
    });

    test("retorna false para ISBN com dígito verificador incorreto", () => {
      expect(isValidISBN10("1234567890")).toBe(false);
    });

    test("retorna false para string com tamanho incorreto", () => {
      expect(isValidISBN10("047195869" )).toBe(false);
    });

    test("retorna false para string vazia", () => {
      expect(isValidISBN10("")).toBe(false);
    });
  });

  describe("validação de formato", () => {
    test("retorna false quando os 9 primeiros caracteres não são dígitos", () => {
      expect(isValidISBN10("04719A8697")).toBe(false);
    });

    test("retorna false quando X aparece antes do último caractere", () => {
      expect(isValidISBN10("0X71958697")).toBe(false);
    });

    test("retorna false para valores que não são string", () => {
      expect(isValidISBN10(471958697)).toBe(false);
    });
  });
});
