# Prompts Utilizados no Trial

**Dev:** pedroseabra27 | **Kata:** kata-06-array-chunking-pagination | **Tratamento:** COM_IA

---

## Prompt 1

> Implemente a função `paginate(items, pageSize, pageNumber)` que recebe um array, o tamanho da página desejado (`pageSize`) e o número da página que quer acessar (`pageNumber`).
>
> A função deve retornar um objeto com a página solicitada e informações de navegação:
> - `data`: os itens daquela página específica.
> - `totalPages`: o total de páginas geradas.
> - `hasNext`: `true` se existir uma próxima página.
> - `hasPrev`: `true` se existir uma página anterior.
>
> Exemplo: `paginate(["A","B","C","D"], 2, 1)` retorna `{ data: ["A","B"], totalPages: 2, hasNext: true, hasPrev: false }`.
>
> Regras adicionais: `pageSize` deve ser inteiro maior que 0. `pageNumber` deve ser inteiro maior que 0. Se a página estiver fora do intervalo, `data` deve ser array vazio. Se a entrada não for válida, lançar erro.

**Resposta da IA:**

```js
function paginate(items, pageSize, pageNumber) {
  if (!Array.isArray(items)) throw new Error("items must be an array");
  if (!Number.isInteger(pageSize) || pageSize <= 0) throw new Error("pageSize must be > 0");
  if (!Number.isInteger(pageNumber) || pageNumber <= 0) throw new Error("pageNumber must be > 0");

  const totalPages = Math.ceil(items.length / pageSize);
  const data = items.slice((pageNumber - 1) * pageSize, pageNumber * pageSize);
  return {
    data,
    totalPages,
    hasNext: pageNumber < totalPages,
    hasPrev: pageNumber > 1 && items.length > 0
  };
}
module.exports = { paginate };
```

A estratégia usa `Math.ceil` para calcular o total de páginas e `Array.slice` para extrair a fatia correta. `hasNext` e `hasPrev` são derivados diretamente do número da página atual versus o total. A validação de entrada cobre arrays inválidos, pageSize e pageNumber não-inteiros ou menores que 1.

Solução aplicada diretamente, sem necessidade de prompts de correção — a suíte de aceite passou de primeira (10/10 testes, `test_attempts: 1`).
