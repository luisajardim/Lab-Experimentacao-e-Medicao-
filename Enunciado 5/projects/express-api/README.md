# express-api (projeto-carga leve)

API Express pequena, escrita à mão (não há template oficial equivalente a `create-vite`/
`create-next-app` para um servidor Express). É o extremo leve dos três projetos-carga: poucas
dependências diretas e nenhum passo de compilação.

- `src/app.js` — rotas `/health`, `/items` e `/items/:id`, com `cors`, `morgan` e `compression`.
- `src/server.js` — sobe o app (`npm start`), usado só manualmente.
- `scripts/build.cjs` — o `build` do experimento: sobe o app numa porta efêmera, bate nas rotas
  e sai com código 0 só se todas responderem. É o critério `build_ok` do runner (T04, #99).
