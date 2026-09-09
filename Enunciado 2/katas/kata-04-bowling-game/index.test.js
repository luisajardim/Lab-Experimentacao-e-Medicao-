const { BowlingGame } = require("./index");

function rollMany(game, count, pins) {
  for (let i = 0; i < count; i++) {
    game.roll(pins);
  }
}

function rollSpare(game) {
  game.roll(5);
  game.roll(5);
}

function rollStrike(game) {
  game.roll(10);
}

describe("BowlingGame", () => {
  let game;

  beforeEach(() => {
    game = new BowlingGame();
  });

  describe("jogos simples", () => {
    test("retorna 0 quando todas as jogadas derrubam 0 pinos", () => {
      rollMany(game, 20, 0);
      expect(game.score()).toBe(0);
    });

    test("soma jogadas sem spare ou strike", () => {
      rollMany(game, 20, 3);
      expect(game.score()).toBe(60);
    });
  });

  describe("spare", () => {
    test("soma bônus do spare com a próxima jogada", () => {
      rollSpare(game);
      game.roll(3);
      rollMany(game, 17, 0);
      expect(game.score()).toBe(16);
    });

    test("calcula múltiplos spares corretamente", () => {
      for (let i = 0; i < 10; i++) {
        rollSpare(game);
      }
      game.roll(5);
      expect(game.score()).toBe(150);
    });
  });

  describe("strike", () => {
    test("soma bônus do strike com as duas próximas jogadas", () => {
      rollStrike(game);
      game.roll(3);
      game.roll(4);
      rollMany(game, 16, 0);
      expect(game.score()).toBe(24);
    });

    test("calcula jogo perfeito (12 strikes)", () => {
      rollMany(game, 12, 10);
      expect(game.score()).toBe(300);
    });
  });

  describe("10º frame", () => {
    test("concede uma jogada bônus após spare no último frame", () => {
      rollMany(game, 18, 0);
      game.roll(5);
      game.roll(5);
      game.roll(7);
      expect(game.score()).toBe(17);
    });

    test("concede duas jogadas bônus após strike no último frame", () => {
      rollMany(game, 18, 0);
      game.roll(10);
      game.roll(3);
      game.roll(4);
      expect(game.score()).toBe(17);
    });
  });

  describe("validação de entrada", () => {
    test("lança erro para número de pinos negativo", () => {
      expect(() => game.roll(-1)).toThrow();
    });

    test("lança erro para número de pinos maior que 10", () => {
      expect(() => game.roll(11)).toThrow();
    });

    test("lança erro para valores não inteiros", () => {
      expect(() => game.roll(3.5)).toThrow();
    });
  });
});
