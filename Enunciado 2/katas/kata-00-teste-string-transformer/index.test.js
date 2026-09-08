const { transformString } = require("./index");

describe("transformString", () => {
  describe("strings simples", () => {
    test("inverte os caracteres de uma única palavra", () => {
      expect(transformString("hello")).toBe("olleh");
    });

    test("inverte os caracteres mantendo a ordem das palavras", () => {
      expect(transformString("hello world")).toBe("olleh dlrow");
    });

    test("funciona com três palavras", () => {
      expect(transformString("one two three")).toBe(
        "eno owt eerht"
      );
    });
  });

  describe("espaços", () => {
    test("remove espaços no início", () => {
      expect(transformString("   hello world")).toBe(
        "olleh dlrow"
      );
    });

    test("remove espaços no final", () => {
      expect(transformString("hello world   ")).toBe(
        "olleh dlrow"
      );
    });

    test("remove espaços no início e no final", () => {
      expect(transformString("   hello world   ")).toBe(
        "olleh dlrow"
      );
    });

    test("reduz múltiplos espaços entre palavras", () => {
      expect(transformString("hello    world")).toBe(
        "olleh dlrow"
      );
    });

    test("trata diferentes combinações de espaços", () => {
      expect(transformString("  hello   beautiful    world  ")).toBe(
        "olleh lufituaeb dlrow"
      );
    });

    test("retorna string vazia para uma string contendo apenas espaços", () => {
      expect(transformString("     ")).toBe("");
    });

    test("retorna string vazia para uma string vazia", () => {
      expect(transformString("")).toBe("");
    });
  });

  describe("caracteres especiais", () => {
    test("preserva pontuação e apenas inverte sua posição", () => {
      expect(transformString("hello! world.")).toBe(
        "!olleh .dlrow"
      );
    });

    test("funciona com números dentro das palavras", () => {
      expect(transformString("abc123 456def")).toBe(
        "321cba fed654"
      );
    });

    test("funciona com caracteres especiais", () => {
      expect(transformString("foo-bar test_case")).toBe(
        "rab-oof esac_tset"
      );
    });
  });

  describe("diferenciação entre maiúsculas e minúsculas", () => {
    test("preserva maiúsculas e minúsculas", () => {
      expect(transformString("Hello World")).toBe(
        "olleH dlroW"
      );
    });

    test("não altera o conteúdo dos caracteres", () => {
      expect(transformString("JavaScript")).toBe(
        "tpircSavaJ"
      );
    });
  });

  describe("validação de entrada", () => {
    test("lança erro para undefined", () => {
      expect(() => transformString(undefined)).toThrow();
    });

    test("lança erro para null", () => {
      expect(() => transformString(null)).toThrow();
    });

    test("lança erro para números", () => {
      expect(() => transformString(12345)).toThrow();
    });

    test("lança erro para booleanos", () => {
      expect(() => transformString(true)).toThrow();
    });

    test("lança erro para objetos", () => {
      expect(() => transformString({ value: "hello" })).toThrow();
    });

    test("lança erro para arrays", () => {
      expect(() => transformString(["hello", "world"])).toThrow();
    });
  });
});