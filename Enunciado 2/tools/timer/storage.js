const fs = require('fs');
const path = require('path');

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
  if (dir && !fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const logs = loadExistingLogs(filePath);
  logs.push(record);
  fs.writeFileSync(filePath, JSON.stringify(logs, null, 2) + '\n', 'utf8');
}

function createRecord({ dev, kata, treatment, startTime, endedAt, testAttempts, success, timeout }) {
  const durationSeconds = (endedAt - startTime) / 1000;
  return {
    trial_id: `${dev}_${kata}_${treatment}`,
    developer: dev,
    kata,
    treatment,
    start_time: new Date(startTime).toISOString(),
    end_time: new Date(endedAt).toISOString(),
    duration_seconds: parseFloat(durationSeconds.toFixed(3)),
    test_attempts: testAttempts,
    success,
    timeout
  };
}

module.exports = { saveTrialLog, createRecord };