const { toRoman } = require("./index");

describe("toRoman", () => {
  describe("símbolos simples", () => {
    test("converte 1 para I", () => {
      expect(toRoman(1)).toBe("I");
    });

    test("converte 5 para V", () => {
      expect(toRoman(5)).toBe("V");
    });

    test("converte 10 para X", () => {
      expect(toRoman(10)).toBe("X");
    });

    test("converte 50 para L", () => {
      expect(toRoman(50)).toBe("L");
    });

    test("converte 100 para C", () => {
      expect(toRoman(100)).toBe("C");
    });

    test("converte 500 para D", () => {
      expect(toRoman(500)).toBe("D");
    });

    test("converte 1000 para M", () => {
      expect(toRoman(1000)).toBe("M");
    });
  });

  describe("símbolos repetidos e somados", () => {
    test("converte 2 para II", () => {
      expect(toRoman(2)).toBe("II");
    });

    test("converte 3 para III", () => {
      expect(toRoman(3)).toBe("III");
    });

    test("converte 6 para VI", () => {
      expect(toRoman(6)).toBe("VI");
    });

    test("converte 8 para VIII", () => {
      expect(toRoman(8)).toBe("VIII");
    });
  });

  describe("casos de subtração", () => {
    test("converte 4 para IV", () => {
      expect(toRoman(4)).toBe("IV");
    });

    test("converte 9 para IX", () => {
      expect(toRoman(9)).toBe("IX");
    });

    test("converte 40 para XL", () => {
      expect(toRoman(40)).toBe("XL");
    });

    test("converte 90 para XC", () => {
      expect(toRoman(90)).toBe("XC");
    });

    test("converte 400 para CD", () => {
      expect(toRoman(400)).toBe("CD");
    });

    test("converte 900 para CM", () => {
      expect(toRoman(900)).toBe("CM");
    });
  });

  describe("números compostos", () => {
    test("converte 58 para LVIII", () => {
      expect(toRoman(58)).toBe("LVIII");
    });

    test("converte 1994 para MCMXCIV", () => {
      expect(toRoman(1994)).toBe("MCMXCIV");
    });

    test("converte 2024 para MMXXIV", () => {
      expect(toRoman(2024)).toBe("MMXXIV");
    });

    test("converte 3999 para MMMCMXCIX", () => {
      expect(toRoman(3999)).toBe("MMMCMXCIX");
    });
  });

  describe("validação de entrada", () => {
    test("lança erro para 0", () => {
      expect(() => toRoman(0)).toThrow();
    });

    test("lança erro para números negativos", () => {
      expect(() => toRoman(-10)).toThrow();
    });

    test("lança erro para números acima de 3999", () => {
      expect(() => toRoman(4000)).toThrow();
    });

    test("lança erro para números não inteiros", () => {
      expect(() => toRoman(3.5)).toThrow();
    });

    test("lança erro para valores que não são números", () => {
      expect(() => toRoman("10")).toThrow();
    });
  });
});
