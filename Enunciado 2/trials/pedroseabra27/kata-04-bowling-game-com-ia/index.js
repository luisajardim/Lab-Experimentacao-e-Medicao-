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
