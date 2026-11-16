// API mínima usada como carga do experimento (T03, #98). Sem estado em disco e sem rede:
// o que importa aqui é exercitar as dependências instaladas pelo gerenciador.
"use strict";

const express = require("express");
const cors = require("cors");
const morgan = require("morgan");
const compression = require("compression");

const ITEMS = [
  { id: 1, manager: "npm", family: "npm" },
  { id: 2, manager: "pnpm", family: "pnpm" },
  { id: 3, manager: "bun", family: "bun" },
  { id: 4, manager: "yarn-classic", family: "yarn" },
  { id: 5, manager: "yarn-berry-nm", family: "yarn" },
  { id: 6, manager: "yarn-berry-pnp", family: "yarn" },
];

function createApp({ quiet = false } = {}) {
  const app = express();
  app.use(compression());
  app.use(cors());
  app.use(express.json());
  if (!quiet) app.use(morgan("tiny"));

  app.get("/health", (_req, res) => res.json({ status: "ok" }));
  app.get("/items", (_req, res) => res.json({ count: ITEMS.length, items: ITEMS }));
  app.get("/items/:id", (req, res) => {
    const item = ITEMS.find((i) => i.id === Number(req.params.id));
    if (!item) return res.status(404).json({ error: "not found" });
    return res.json(item);
  });
  app.use((_req, res) => res.status(404).json({ error: "not found" }));

  return app;
}

module.exports = { createApp, ITEMS };
