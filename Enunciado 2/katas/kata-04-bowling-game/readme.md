# Kata 04 — Bowling Game

## Enunciado

Implemente a classe `BowlingGame`, que simula a pontuação de uma partida de boliche, com os seguintes métodos:

- `roll(pins)`: registra uma jogada, informando a quantidade de pinos derrubados (`0` a `10`).
- `score()`: retorna a pontuação total da partida, considerando todas as jogadas registradas até o momento.

### Regras de pontuação

- Uma partida tem **10 frames**.
- Em cada frame, o jogador tem até **2 jogadas** para derrubar os 10 pinos, exceto no 10º frame (ver abaixo).
- **Frame normal:** a pontuação do frame é a soma dos pinos derrubados nas duas jogadas.
- **Spare** (derrubar os 10 pinos em duas jogadas): a pontuação do frame é `10` + o número de pinos derrubados na **próxima jogada**.
- **Strike** (derrubar os 10 pinos na primeira jogada do frame): a pontuação do frame é `10` + o número de pinos derrubados nas **duas próximas jogadas**.
- **10º frame:** se o jogador fizer *spare* ou *strike*, ganha jogada(s) bônus adicionais (respectivamente 1 ou 2) apenas para fins de cálculo de pontuação, sem formar frames adicionais.

### Exemplo

```js
const game = new BowlingGame();

// Jogo "perfeito": 12 strikes seguidos
for (let i = 0; i < 12; i++) {
  game.roll(10);
}

game.score(); // 300
```

```js
const game = new BowlingGame();

// Todas as jogadas derrubam 0 pinos
for (let i = 0; i < 20; i++) {
  game.roll(0);
}

game.score(); // 0
```

### Regras adicionais

- `roll(pins)` deve lançar um erro se `pins` for menor que `0`, maior que `10`, ou não for um número inteiro.
