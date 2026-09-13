function formatTime(totalSeconds) {
  const m = Math.floor(totalSeconds / 60);
  const s = Math.floor(totalSeconds % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function clearScreen() {
  process.stdout.write('\x1b[2J\x1b[H');
}

function drawHeader({ dev, kata, treatment, timeboxMinutes, elapsedSeconds, timeboxSeconds, testAttempts }) {
  const progress = Math.min(1, elapsedSeconds / timeboxSeconds);
  const barLen = 30;
  const filled = Math.round(barLen * progress);
  const empty = barLen - filled;
  const bar = '█'.repeat(filled) + '░'.repeat(empty);

  const header = [
    '=== TRIAL TIMER ===',
    `Dev:        ${dev}`,
    `Kata:       ${kata}`,
    `Tratamento: ${treatment}`,
    `Timebox:    ${timeboxMinutes} min`,
    `Tentativas: ${testAttempts}`,
    '',
    `⏳  ${formatTime(elapsedSeconds)} / ${formatTime(timeboxSeconds)} | [${bar}] ${Math.round(progress * 100)}%`,
    '',
    'Pressione Shift+T para rodar testes | Ctrl+C para abortar',
    ''
  ].join('\n');

  process.stdout.write(header);
}

module.exports = { formatTime, clearScreen, drawHeader };