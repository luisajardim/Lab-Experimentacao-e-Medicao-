class BowlingGame {
  constructor() {
    this.frames = [];
    this.currentFrame = 0;
    this.currentRoll = 0;
  }

  roll(pins) {
    // Validações
    if (Number.isNaN(pins) || !Number.isInteger(pins) || pins < 0 || pins > 10) {
      throw('Valores invalidos para pinos derrubados.');
    }

    // 10º frame
    if (this.currentFrame === 9) {

      // Primeira jogada do 10º frame
      if (this.currentRoll === 0) {

        this.frames.push({
          downed: pins,
          remains: 10 - pins,
          rolls: 0,
          bonusRolls: []
        });

        // Strike: ganha 2 jogadas bônus
        if (pins === 10) {
          this.frames[9].bonusRolls = [];
        }
      }

      // Segunda jogada do 10º frame
      else if (this.currentRoll === 1) {

        const frame = this.frames[9];

        frame.downed += pins;
        frame.remains = 10 - frame.downed;
        frame.rolls = 1;

        // Spare: ganha 1 jogada bônus
        if (frame.downed === 10) {
          frame.bonusRolls = [];
        }

        // Se não foi spare, o jogo termina
        if (frame.downed < 10) {
          this.currentFrame += 1;
        }
      }

      // Jogadas bônus do 10º frame
      else {

        const frame = this.frames[9];

        // Strike no 10º frame permite 2 bônus
        if (frame.rolls === 0) {
          frame.bonusRolls.push(pins);

          if (frame.bonusRolls.length === 2) {
            this.currentFrame += 1;
          }
        }

        // Spare no 10º frame permite 1 bônus
        else if (frame.downed === 10) {
          frame.bonusRolls.push(pins);
          this.currentFrame += 1;
        }
      }

      this.currentRoll += 1;
      return;
    }

    // Frames normais
    if (this.currentRoll === 0) {
      this.frames.push({
        downed: pins,
        remains: 10 - pins,
        rolls: 0
      });

    } else {
      const frame = this.frames[this.currentFrame];
      const downed = frame.downed + pins;

      this.frames[this.currentFrame] = {
        downed,
        remains: 10 - downed,
        rolls: 1
      };
    }

    this.currentRoll += 1;

    // Strike ou segunda jogada
    if (this.currentRoll === 2 || pins === 10) {
      this.currentFrame += 1;
      this.currentRoll = 0;
    }
  }

  score() {
    let score = 0;
    this.frames.forEach((frame, index) => {
      // 10º frame
      if (index === 9) {

        score += frame.downed;

        frame.bonusRolls.forEach(pins => {
          score += pins;
        });

        return;
      }

      // Strike
      if (frame.rolls === 0 && frame.downed === 10) {
        const nextFrame = this.frames[index + 1];

        if (nextFrame) {
          score += 10 + nextFrame.downed;

          // Se o próximo frame também for strike,
          // precisamos da jogada seguinte
          if (nextFrame.rolls === 0) {
            const followingFrame = this.frames[index + 2];

            if (followingFrame) {
              score += followingFrame.downed;
            }
          } else {
            score += nextFrame.remains;
          }
        }

      // Spare
      } else if (frame.rolls === 1 && frame.downed === 10) {
        const nextFrame = this.frames[index + 1];

        if (nextFrame) {
          score += 10 + nextFrame.downed;
        }

      // Frame normal
      } else {
        score += frame.downed;
      }
    });

    return score;
  }
}

module.exports = { BowlingGame };