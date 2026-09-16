# Prompts Utilizados no Trial

**Dev:** luisajardim | **Kata:** kata-05-isbn-10-validator | **Tratamento:** COM_IA

---

## Prompt 1

> Implemente a função `isValidISBN10(isbn)` que recebe uma string com um código ISBN-10 e retorna `true` se o código for válido, ou `false` caso contrário.
>
> Regra: multiplique o 1º dígito por 10, o 2º por 9, o 3º por 8, e assim por diante até o último caractere, que vale 1. Some todos os resultados. Se a soma for divisível por 11, o ISBN é válido.
>
> Regra especial: o último caractere pode ser um X, e nesse caso vale 10. O código deve ter exatamente 10 caracteres. Os 9 primeiros caracteres devem ser dígitos de 0 a 9.
>
> Exemplos: isValidISBN10("0471958697") = true, isValidISBN10("047195869X") = false, isValidISBN10("0306406152") = true, isValidISBN10("097522980X") = true.
>
> Regra adicional: se a entrada não for uma string válida com 10 caracteres no formato esperado, a função deve retornar false (não lançar erro).

**Resposta da IA:**

```js
function isValidISBN10(isbn) {
  if (typeof isbn !== "string" || isbn.length !== 10) {
    return false;
  }

  let sum = 0;
  for (let i = 0; i < 10; i++) {
    const char = isbn[i];
    let digit;

    if (char >= "0" && char <= "9") {
      digit = Number(char);
    } else if (char === "X" && i === 9) {
      digit = 10;
    } else {
      return false;
    }

    sum += digit * (10 - i);
  }

  return sum % 11 === 0;
}

module.exports = { isValidISBN10 };
```

Abordagem: valida primeiro o tipo e o tamanho (retorna `false` cedo se não for string de 10 caracteres). Depois percorre cada posição: se for dígito `0`-`9`, converte pra número; se for `X` e estiver na última posição (índice 9), vale 10; qualquer outro caractere (incluindo `X` fora da última posição) invalida o ISBN. Multiplica cada valor pelo peso `10 - i` (10, 9, 8, ..., 1) e soma. No final, verifica se a soma é divisível por 11.

Solução aplicada diretamente, sem necessidade de prompts de correção — a suíte de aceite passou de primeira (10/10 testes, `test_attempts: 1`).
