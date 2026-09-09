# Kata 01 — FizzBuzz

## Enunciado

Implemente a função `fizzbuzz(n)` que recebe um número inteiro positivo `n` e retorna um **array de strings** com os números de `1` até `n`, seguindo as regras abaixo:

- Se o número for múltiplo de **3**, o item deve ser a string `"Fizz"`.
- Se o número for múltiplo de **5**, o item deve ser a string `"Buzz"`.
- Se o número for múltiplo de **3 e de 5** ao mesmo tempo, o item deve ser a string `"FizzBuzz"`.
- Caso contrário, o item deve ser o próprio número, convertido para string.

### Exemplo

```js
fizzbuzz(15);
// [
//   "1", "2", "Fizz", "4", "Buzz",
//   "Fizz", "7", "8", "Fizz", "Buzz",
//   "11", "Fizz", "13", "14", "FizzBuzz"
// ]
```

### Regras adicionais

- Se `n` for `0`, retorne um array vazio `[]`.
- Se `n` for negativo ou não for um número inteiro, a função deve lançar um erro (`throw`).
