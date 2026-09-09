const { fizzbuzz } = require("./index");

describe("fizzbuzz", () => {
  describe("casos básicos", () => {
    test("retorna array vazio para n = 0", () => {
      expect(fizzbuzz(0)).toEqual([]);
    });

    test("retorna ['1'] para n = 1", () => {
      expect(fizzbuzz(1)).toEqual(["1"]);
    });

    test("retorna números como string quando não são múltiplos de 3 ou 5", () => {
      expect(fizzbuzz(2)).toEqual(["1", "2"]);
    });
  });

  describe("múltiplos de 3", () => {
    test("retorna Fizz para 3", () => {
      expect(fizzbuzz(3)).toEqual(["1", "2", "Fizz"]);
    });

    test("retorna Fizz para 9", () => {
      const result = fizzbuzz(9);
      expect(result[8]).toBe("Fizz");
    });
  });

  describe("múltiplos de 5", () => {
    test("retorna Buzz para 5", () => {
      expect(fizzbuzz(5)).toEqual(["1", "2", "Fizz", "4", "Buzz"]);
    });

    test("retorna Buzz para 20", () => {
      const result = fizzbuzz(20);
      expect(result[19]).toBe("Buzz");
    });
  });

  describe("múltiplos de 3 e 5", () => {
    test("retorna FizzBuzz para 15", () => {
      const result = fizzbuzz(15);
      expect(result[14]).toBe("FizzBuzz");
    });

    test("retorna FizzBuzz para 30", () => {
      const result = fizzbuzz(30);
      expect(result[29]).toBe("FizzBuzz");
    });
  });

  describe("sequência completa", () => {
    test("gera a sequência correta de 1 a 15", () => {
      expect(fizzbuzz(15)).toEqual([
        "1",
        "2",
        "Fizz",
        "4",
        "Buzz",
        "Fizz",
        "7",
        "8",
        "Fizz",
        "Buzz",
        "11",
        "Fizz",
        "13",
        "14",
        "FizzBuzz",
      ]);
    });

    test("possui o tamanho igual a n", () => {
      expect(fizzbuzz(50)).toHaveLength(50);
    });
  });

  describe("validação de entrada", () => {
    test("lança erro para números negativos", () => {
      expect(() => fizzbuzz(-5)).toThrow();
    });

    test("lança erro para números não inteiros", () => {
      expect(() => fizzbuzz(3.5)).toThrow();
    });

    test("lança erro para valores que não são números", () => {
      expect(() => fizzbuzz("15")).toThrow();
    });

    test("lança erro para undefined", () => {
      expect(() => fizzbuzz(undefined)).toThrow();
    });
  });
});
