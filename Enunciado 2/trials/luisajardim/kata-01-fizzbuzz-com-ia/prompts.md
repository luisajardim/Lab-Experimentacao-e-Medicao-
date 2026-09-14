# Prompts Utilizados no Trial

**Dev:** luisajardim | **Kata:** kata-01-fizzbuzz | **Tratamento:** COM_IA

---

## Prompt 1

> Implemente a função `fizzbuzz(n)` que recebe um número inteiro positivo `n` e retorna um array de strings com os números de 1 até n, seguindo as regras abaixo:
> - Se o número for múltiplo de 3, o item deve ser a string "Fizz".
> - Se o número for múltiplo de 5, o item deve ser a string "Buzz".
> - Se o número for múltiplo de 3 e de 5 ao mesmo tempo, o item deve ser a string "FizzBuzz".
> - Caso contrário, o item deve ser o próprio número, convertido para string.
>
> Regras adicionais: se n for 0, retorne um array vazio []. Se n for negativo ou não for um número inteiro, a função deve lançar um erro (throw).

**Resposta da IA:**

```js
function fizzbuzz(n) {
  if (typeof n !== "number" || !Number.isInteger(n) || n < 0) {
    throw new TypeError("n must be a non-negative integer");
  }

  const result = [];
  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) result.push("FizzBuzz");
    else if (i % 3 === 0) result.push("Fizz");
    else if (i % 5 === 0) result.push("Buzz");
    else result.push(String(i));
  }
  return result;
}

module.exports = { fizzbuzz };
```

Solução aplicada diretamente, sem necessidade de prompts de correção — a suíte de aceite passou de primeira (15/15 testes, `test_attempts: 1`).
