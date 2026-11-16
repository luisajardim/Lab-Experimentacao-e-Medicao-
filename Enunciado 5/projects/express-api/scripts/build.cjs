// "build" da API: prova que a instalação funciona (critério build_ok do runner, T04).
// Sobe o app numa porta efêmera, bate em /health e /items e sai 0 só se as duas responderem.
// Não é cronometrado; também não usa rede externa (só localhost).
"use strict";

const http = require("node:http");
const assert = require("node:assert/strict");

const { createApp, ITEMS } = require("../src/app");

function get(port, path) {
  return new Promise((resolve, reject) => {
    const req = http.get({ host: "127.0.0.1", port, path }, (res) => {
      let body = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => resolve({ status: res.statusCode, body }));
    });
    req.on("error", reject);
  });
}

async function main() {
  const server = createApp({ quiet: true }).listen(0, "127.0.0.1");
  await new Promise((resolve, reject) => {
    server.once("listening", resolve);
    server.once("error", reject);
  });
  try {
    const { port } = server.address();
    const health = await get(port, "/health");
    assert.equal(health.status, 200);
    assert.deepEqual(JSON.parse(health.body), { status: "ok" });

    const items = await get(port, "/items");
    assert.equal(items.status, 200);
    assert.equal(JSON.parse(items.body).count, ITEMS.length);

    const missing = await get(port, "/items/999");
    assert.equal(missing.status, 404);
  } finally {
    server.close();
  }
  console.log("build ok: express-api responde em /health, /items e /items/:id");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
