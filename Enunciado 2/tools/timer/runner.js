const { spawnSync } = require('child_process');

function executeTestCommand(cmd) {
  const startRun = Date.now();
  const result = spawnSync(cmd, { shell: true, encoding: 'utf8', stdio: 'inherit' });
  const durationRun = (Date.now() - startRun) / 1000;

  return {
    passed: result.status === 0,
    duration: durationRun
  };
}

function waitForKey() {
  return new Promise((resolve) => {
    const onKey = () => {
      process.stdin.removeListener('data', onKey);
      resolve();
    };
    process.stdin.on('data', onKey);
  });
}

module.exports = { executeTestCommand, waitForKey };