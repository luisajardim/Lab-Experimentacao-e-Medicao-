# Validação da coleta completa (T13, #110)

Gerado por `uv run lab05 validate` (`src/validate.py`). Não edite à mão.

Dataset congelado: `data/processed/runs_all.csv`, 2166 linhas (2160 medidas e 6 de aquecimento), sha256 `4598d73860184c57b7ee1806c2447ea58dd88b8310acb7dd4b243efe0a2f6669`. Os hashes das fontes estão em `data/processed/manifest.json`; `uv run lab05 validate --check` confere se nada mudou.

Nenhuma linha foi removida. Falhas e medições extremas ficam no dataset e são só registradas aqui (ver C2 em `ameacas.md`).

## Máquinas

| Máquina | Linhas | Início | Fim | CPU | RAM (livre no início) | Build | Energia | Disco |
|---|---|---|---|---|---|---|---|---|
| `bernardo` | 722 | 2026-11-23T09:54:13-03:00 | 2026-11-23T13:53:26-03:00 | AMD Ryzen 5 5500 | 15.9 GB (6.39 GB) | 26200 | Alto desempenho | SSD,SSD,HDD,SSD |
| `luisa` | 722 | 2026-11-24T13:39:21-03:00 | 2026-11-24T18:41:15-03:00 | 13th Gen Intel(R) Core(TM) i5-13450HX | 7.69 GB (0.34 GB) | 26200 | Alto desempenho | SSD |
| `pedro` | 722 | 2026-11-24T23:04:20-03:00 | 2026-11-25T04:33:20-03:00 | 12th Gen Intel(R) Core(TM) i5-12450H | 15.73 GB (6.62 GB) | 26100 | Legion Performance Mode | SSD |

## Checagens

| Checagem | Situação | Resultado |
|---|---|---|
| Desenho completo | ok | 3 máquinas × 72 células × 10 repetições + 2 aquecimentos por máquina |
| Versões iguais nas máquinas | ok | Node 24.22.3; npm 11.19.1, pnpm 12.21.0, bun 1.4.4, yarn-classic 1.22.22, yarn-berry-nm 4.18.1, yarn-berry-pnp 4.18.1 |
| Registry local | ok | todas as linhas com registry `local` |
| Instalações válidas | ok | 2166 de 2166 com `exit_code = 0` e `build_ok` |
| Mesma árvore instalada nas máquinas (I1) | ok | `n_files` igual entre as máquinas em 72 de 72 células |
| Medições extremas (registradas, mantidas) | aviso | 11 de 1450 medições em células com mediana ≥ 1 s passaram de 3× a mediana |
| Pausas durante a coleta | aviso | 1 lacuna(s) de mais de 5 min entre duas medições seguidas |

### Medições extremas (registradas, mantidas)

- `bernardo` react-vite ci npm rep 2: 16.60 s (mediana 2.84 s, 5.8×)
- `bernardo` react-vite ci npm rep 5: 11.44 s (mediana 2.84 s, 4.0×)
- `luisa` express-api cold npm rep 1: 13.30 s (mediana 2.66 s, 5.0×)
- `luisa` express-api cold npm rep 5: 11.10 s (mediana 2.66 s, 4.2×)
- `luisa` express-api ci npm rep 5: 4.96 s (mediana 1.53 s, 3.2×)
- `luisa` express-api ci npm rep 6: 10.49 s (mediana 1.53 s, 6.8×)
- `luisa` next-app warm-cache yarn-berry-pnp rep 6: 5.70 s (mediana 1.69 s, 3.4×)
- `luisa` express-api cold npm rep 7: 11.73 s (mediana 2.66 s, 4.4×)
- `luisa` express-api ci npm rep 9: 12.81 s (mediana 1.53 s, 8.4×)
- `luisa` express-api cold npm rep 10: 11.74 s (mediana 2.66 s, 4.4×)
- `pedro` express-api cold npm rep 4: 7.89 s (mediana 2.51 s, 3.1×)

### Pausas durante a coleta

- `luisa`: 39.7 min entre 2026-11-24T14:14:08-03:00 e 2026-11-24T14:53:49-03:00; a medição seguinte (next-app ci yarn-berry-pnp rep 2) levou 21.21 s
