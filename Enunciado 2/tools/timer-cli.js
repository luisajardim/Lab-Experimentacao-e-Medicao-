#!/usr/bin/env node

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// ---------- Argument parsing ----------
function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = args[i + 1];
    if (next && !next.startsWith('--')) {
      parsed[key] = next;
      i++;
    } else {
      parsed[key] = true;
    }
  }
  return parsed;
}

const cli = parseArgs();

if (!cli.dev || !cli.kata || !cli.treatment || !cli.cmd) {
  console.error('Uso: node tools/timer-cli.js --dev <devId> --kata <kataId> --treatment <COM_IA|SEM_IA> --cmd "<comando>" [--timebox <min>] [--output <arquivo.json>]');
  process.exit(1);
}

const dev = String(cli.dev).trim();
const kata = String(cli.kata).trim();
const treatment = String(cli.treatment).trim();
const cmd = String(cli.cmd).trim();
const timeboxMinutes = Number(cli.timebox ?? 35);
const outputPath = String(cli.output ?? 'data/trials-log.json').trim();

if (!['COM_IA', 'SEM_IA'].includes(treatment)) {
  console.error('Tratamento inválido. Use COM_IA ou SEM_IA.');
  process.exit(1);
}

// ---------- Helpers ----------
function formatTime(totalSeconds) {
  const m = Math.floor(totalSeconds / 60);
  const s = Math.floor(totalSeconds % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function clearScreen() {
  process.stdout.write('\x1b[2J\x1b[H');
}

function drawHeader(elapsedSeconds, timeboxSeconds, testAttempts) {
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

// ---------- JSON persistence ----------
function loadExistingLogs(filePath) {
  if (!fs.existsSync(filePath)) return [];
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveTrialLog(filePath, record) {
  const dir = path.dirname(filePath);
  if (!dir && !fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  if (dir && !fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const logs = loadExistingLogs(filePath);
  logs.push(record);
  fs.writeFileSync(filePath, JSON.stringify(logs, null, 2) + '\n', 'utf8');
}

function finishTrial(endedAt) {
  const durationSeconds = (endedAt - startTime) / 1000;
  const record = {
    trial_id: `${dev}_${kata}_${treatment}`,
    developer: dev,
    kata,
    treatment,
    start_time: new Date(startTime).toISOString(),
    end_time: new Date(endedAt).toISOString(),
    duration_seconds: parseFloat(durationSeconds.toFixed(3)),
    test_attempts: testAttempts + 1,
    success,
    timeout
  };
  saveTrialLog(outputPath, record);
  return record;
}

// ---------- Main ----------
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

function waitForKey() {
  return new Promise((resolve) => {
    const onKey = (key) => {
      process.stdin.removeListener('data', onKey);
      resolve();
    };
    process.stdin.on('data', onKey);
  });
}

function runTests() {
  if (testLocked) return;
  testLocked = true;
  testRunning = true;

  console.log('\n🧪 Executando testes...\n');

  const startRun = Date.now();
  const result = spawnSync(cmd, { shell: true, encoding: 'utf8', stdio: 'inherit' });
  const durationRun = (Date.now() - startRun) / 1000;

  if (result.status === 0) {
    success = true;
    timeout = false;
    const record = finishTrial(Date.now());
    console.log(`\n✅ Testes passaram em ${formatTime(durationRun)} (${durationRun.toFixed(1)}s).`);
    console.log(`💾 Trial salvo em: ${path.resolve(outputPath)}`);
    console.log(`📊 trial_id: ${record.trial_id} | duration_seconds: ${record.duration_seconds} | test_attempts: ${record.test_attempts}`);
    gracefulExit();
    process.exit(0);
  } else {
    testAttempts++;
    console.log('\n❌ Testes falharam. Ajuste seu código e pressione qualquer tecla para continuar...');
    waitForKey().then(() => {
      testRunning = false;
      testLocked = false;
      clearScreen();
    });
  }
}

// ---------- Input handling ----------
process.stdin.setRawMode(true);
process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', (key) => {
  if (!running) return;
  if (key === '\x03') {
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

// ---------- Timer loop ----------
clearScreen();
drawHeader(0, timeboxSeconds, 0);

intervalId = setInterval(() => {
  if (!running) return;
  elapsedSeconds = (Date.now() - startTime) / 1000;

  if (!testRunning) {
    clearScreen();
    drawHeader(elapsedSeconds, timeboxSeconds, testAttempts);
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
