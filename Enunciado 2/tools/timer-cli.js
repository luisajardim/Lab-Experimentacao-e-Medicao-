#!/usr/bin/env node

const path = require('path');

const { parseArgs } = require('./utils');
const { formatTime, clearScreen, drawHeader } = require('./timer/ui');
const { saveTrialLog, createRecord } = require('./timer/storage');
const { executeTestCommand, waitForKey } = require('./timer/runner');

const cli = parseArgs();

if (!cli.dev || !cli.kata || !cli.treatment || !cli.cmd) {
  console.error('Uso: npm run timer -- --dev <devId> --kata <kataId> --treatment <COM_IA|SEM_IA> --cmd "<comando>" [--timebox <min>] [--output <arquivo.json>]');
  process.exit(1);
}

const dev = String(cli.dev).trim();
const kata = String(cli.kata).trim();
const treatment = String(cli.treatment).trim();
const cmd = String(cli.cmd).trim();
const timeboxMinutes = Number(cli.timebox ?? 25);
const outputPath = String(cli.output ?? 'data/trials-log.json').trim();

if (!['COM_IA', 'SEM_IA'].includes(treatment)) {
  console.error('❌ Tratamento inválido. Use COM_IA ou SEM_IA.');
  process.exit(1);
}

// State Control
const startTime = Date.now();
const timeboxSeconds = timeboxMinutes * 60;
let elapsedSeconds = 0;
let testAttempts = 0;
let success = false;
let timeout = false;
let intervalId = null;
let running = true;
let testLocked = false;
let testRunning = false;

function gracefulExit() {
  running = false;
  if (intervalId) clearInterval(intervalId);
  try {
    process.stdin.setRawMode(false);
  } catch {}
  process.stdin.pause();
}

function finishTrial(endedAt) {
  const record = createRecord({
    dev, kata, treatment, startTime, endedAt, testAttempts, success, timeout
  });
  saveTrialLog(outputPath, record);
  return record;
}

function runTests() {
  if (testLocked) return;
  testLocked = true;
  testRunning = true;
  testAttempts++;

  console.log('\n🧪 Executando testes...\n');

  const { passed, duration } = executeTestCommand(cmd);

  if (passed) {
    success = true;
    timeout = false;
    const record = finishTrial(Date.now());
    console.log(`\n✅ Testes passaram em ${formatTime(duration)} (${duration.toFixed(1)}s).`);
    console.log(`💾 Trial salvo em: ${path.resolve(outputPath)}`);
    console.log(`📊 trial_id: ${record.trial_id} | duration_seconds: ${record.duration_seconds} | test_attempts: ${record.test_attempts}`);
    gracefulExit();
    process.exit(0);
  } else {
    console.log('\n❌ Testes falharam. Ajuste seu código e pressione qualquer tecla para continuar...');
    waitForKey().then(() => {
      testRunning = false;
      testLocked = false;
      clearScreen();
    });
  }
}

// Input listeners
process.stdin.setRawMode(true);
process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', (key) => {
  if (!running) return;
  if (key === '\x03') { /* Ctrl+C */
    const record = finishTrial(Date.now());
    clearScreen();
    console.log('🛑 Trial abortado pelo usuário.');
    console.log(`💾 Log parcial salvo em: ${path.resolve(outputPath)}`);
    console.log(`📊 trial_id: ${record.trial_id} | duration_seconds: ${record.duration_seconds} | success: false | timeout: false`);
    gracefulExit();
    process.exit(0);
  }
  if (key === 'T') {
    runTests();
  }
});

process.on('SIGINT', () => {
  const record = finishTrial(Date.now());
  clearScreen();
  console.log('🛑 Trial abortado (SIGINT).');
  console.log(`💾 Log parcial salvo em: ${path.resolve(outputPath)}`);
  gracefulExit();
  process.exit(0);
});

// Start loop
clearScreen();
drawHeader({ dev, kata, treatment, timeboxMinutes, elapsedSeconds: 0, timeboxSeconds, testAttempts });

intervalId = setInterval(() => {
  if (!running) return;
  elapsedSeconds = (Date.now() - startTime) / 1000;

  if (!testRunning) {
    clearScreen();
    drawHeader({ dev, kata, treatment, timeboxMinutes, elapsedSeconds, timeboxSeconds, testAttempts });
  }

  if (elapsedSeconds >= timeboxSeconds) {
    timeout = true;
    success = false;
    const record = finishTrial(Date.now());
    clearScreen();
    console.log('⏰ Tempo esgotado!');
    console.log(`💾 Log de timeout salvo em: ${path.resolve(outputPath)}`);
    console.log(`📊 trial_id: ${record.trial_id} | duration_seconds: ${record.duration_seconds} | success: false | timeout: true`);
    gracefulExit();
    process.exit(0);
  }
}, 1000);