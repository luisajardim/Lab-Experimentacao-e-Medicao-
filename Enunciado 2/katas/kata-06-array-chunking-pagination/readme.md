# Kata 06 — Array Chunking & Pagination

## Enunciado

Implemente a função `paginate(items, pageSize, pageNumber)` que recebe um **array**, o tamanho da página desejado (`pageSize`) e o número da página que quer acessar (`pageNumber`).

A função deve retornar um objeto com a página solicitada e informações de navegação:

- `data`: os itens daquela página específica.
- `totalPages`: o total de páginas geradas.
- `hasNext`: `true` se existir uma próxima página.
- `hasPrev`: `true` se existir uma página anterior.

### Exemplo

```js
paginate(["A", "B", "C", "D"], 2, 1);
// {
//   data: ["A", "B"],
//   totalPages: 2,
//   hasNext: true,
//   hasPrev: false
// }
```

### Regras adicionais

- `pageSize` deve ser um número inteiro maior que `0`.
- `pageNumber` deve ser um número inteiro maior que `0`.
- Se a página solicitada estiver fora do intervalo, `data` deve ser um array vazio.
- Se a entrada não for válida, a função deve lançar um erro (`throw`).
