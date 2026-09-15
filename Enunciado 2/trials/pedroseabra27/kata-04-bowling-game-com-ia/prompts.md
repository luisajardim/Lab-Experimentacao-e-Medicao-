# Prompts Utilizados no Trial

**Dev:** pedroseabra27 | **Kata:** kata-04-bowling-game | **Tratamento:** COM_IA

---

## Prompt 1

> Implemente a classe `BowlingGame`, que simula a pontuação de uma partida de boliche, com os seguintes métodos:
>
> - `roll(pins)`: registra uma jogada, informando a quantidade de pinos derrubados (0 a 10).
> - `score()`: retorna a pontuação total da partida, considerando todas as jogadas registradas até o momento.
>
> Regras: uma partida tem 10 frames. Spare (derrubar 10 em duas jogadas): pontuação do frame é 10 + próxima jogada. Strike (derrubar 10 na primeira): pontuação do frame é 10 + duas próximas jogadas. No 10º frame, spare ou strike garantem jogada(s) bônus apenas para cálculo.
>
> Exemplos: jogo perfeito (12 strikes) = 300. Todas as jogadas com 0 pinos = 0.
>
> Regra adicional: `roll(pins)` deve lançar um erro se `pins` for menor que 0, maior que 10, ou não for um número inteiro.

**Resposta da IA:**

```js
class BowlingGame {
  constructor() {
    this.rolls = [];
  }

  roll(pins) {
    if (!Number.isInteger(pins) || pins < 0 || pins > 10) {
      throw new Error("Invalid pins");
    }
    this.rolls.push(pins);
  }

  score() {
    let score = 0;
    let rollIndex = 0;

    for (let frame = 0; frame < 10; frame++) {
      if (rollIndex >= this.rolls.length) break;

      if (this.rolls[rollIndex] === 10) {
        score += 10 + (this.rolls[rollIndex + 1] || 0) + (this.rolls[rollIndex + 2] || 0);
        rollIndex += 1;
      } else if ((this.rolls[rollIndex] || 0) + (this.rolls[rollIndex + 1] || 0) === 10) {
        score += 10 + (this.rolls[rollIndex + 2] || 0);
        rollIndex += 2;
      } else {
        score += (this.rolls[rollIndex] || 0) + (this.rolls[rollIndex + 1] || 0);
        rollIndex += 2;
      }
    }
    return score;
  }
}

module.exports = { BowlingGame };
```

A estratégia é percorrer os 10 frames mantendo um índice de jogadas. Para strikes, avança 1 posição e soma os bônus das 2 jogadas seguintes. Para spares, avança 2 posições e soma o bônus da próxima. O 10º frame é tratado naturalmente pelo mesmo loop, com as jogadas bônus já presentes no array de rolls.

Solução aplicada diretamente, sem necessidade de prompts de correção — a suíte de aceite passou de primeira (11/11 testes, `test_attempts: 1`).
