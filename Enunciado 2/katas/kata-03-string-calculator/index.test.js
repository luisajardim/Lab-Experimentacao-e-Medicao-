const { add } = require("./index");

describe("add", () => {
  describe("casos básicos", () => {
    test("retorna 0 para string vazia", () => {
      expect(add("")).toBe(0);
    });

    test("retorna o próprio número para um único valor", () => {
      expect(add("1")).toBe(1);
    });

    test("retorna a soma de dois números", () => {
      expect(add("1,2")).toBe(3);
    });
  });

  describe("quantidade qualquer de números", () => {
    test("soma três números", () => {
      expect(add("1,2,3")).toBe(6);
    });

    test("soma cinco números", () => {
      expect(add("1,2,3,4,5")).toBe(15);
    });

    test("soma muitos números", () => {
      expect(add("1,2,3,4,5,6,7,8,9,10")).toBe(55);
    });
  });

  describe("quebras de linha como delimitador", () => {
    test("aceita quebra de linha entre números", () => {
      expect(add("1\n2,3")).toBe(6);
    });

    test("aceita múltiplas quebras de linha", () => {
      expect(add("1\n2\n3")).toBe(6);
    });
  });

  describe("delimitador customizado", () => {
    test("aceita delimitador customizado de um caractere", () => {
      expect(add("//;\n1;2")).toBe(3);
    });

    test("aceita delimitador customizado com múltiplos números", () => {
      expect(add("//;\n1;2;3;4")).toBe(10);
    });

    test("aceita delimitador customizado diferente de ponto e vírgula", () => {
      expect(add("//|\n2|3|4")).toBe(9);
    });
  });

  describe("números negativos", () => {
    test("lança erro contendo o número negativo informado", () => {
      expect(() => add("1,-2,3")).toThrow(/-2/);
    });

    test("lança erro contendo todos os números negativos informados", () => {
      expect(() => add("1,-2,-3,4")).toThrow(/-2.*-3|-3.*-2/);
    });
  });

  describe("valores extras", () => {
    test("ignora espaços em branco ao redor dos números", () => {
      expect(add("1, 2")).toBe(3);
    });

    test("trata zero corretamente", () => {
      expect(add("0,1")).toBe(1);
    });
  });
});
