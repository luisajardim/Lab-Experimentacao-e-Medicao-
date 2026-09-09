# Kata 05 — ISBN-10 Validator

## Enunciado

Implemente a função `isValidISBN10(isbn)` que recebe uma **string** com um código ISBN-10 e retorna `true` se o código for válido, ou `false` caso contrário.

Para validar o ISBN-10, siga a regra abaixo:

- Multiplique o 1º dígito por **10**.
- Multiplique o 2º dígito por **9**.
- Multiplique o 3º dígito por **8**.
- Continue a sequência até o último caractere, que vale **1**.
- Some todos os resultados.
- Se a soma for divisível por **11**, o ISBN é válido.

### Regra especial

- O último caractere pode ser um **`X`**, e nesse caso ele vale **10**.
- O código deve ter exatamente **10 caracteres**.
- Os 9 primeiros caracteres devem ser dígitos de `0` a `9`.

### Exemplos

```js
isValidISBN10("0471958697"); // true
isValidISBN10("047195869X"); // false
isValidISBN10("0306406152"); // true
isValidISBN10("030640615X"); // true
```

### Regras adicionais

- Se a entrada não for uma string válida com 10 caracteres no formato esperado, a função deve retornar `false`.
