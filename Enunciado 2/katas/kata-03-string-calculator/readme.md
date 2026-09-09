# Kata 03 — String Calculator

## Enunciado

Implemente a função `add(numbers)` que recebe uma **string** de números separados por delimitadores e retorna a **soma** desses números.

Siga a evolução de regras abaixo (todas devem ser suportadas simultaneamente na versão final):

1. A função aceita uma string vazia e retorna `0`.
2. A função aceita **1 ou 2 números**, separados por vírgula, e retorna sua soma.
   Ex.: `add("1,2")` retorna `3`.
3. A função aceita uma **quantidade qualquer** de números, separados por vírgula.
   Ex.: `add("1,2,3,4,5")` retorna `15`.
4. A função aceita **quebras de linha (`\n`)** entre os números, além de vírgulas, como delimitadores.
   Ex.: `add("1\n2,3")` retorna `6`.
5. A função aceita um **delimitador customizado**, informado na primeira linha da string no formato `//[delimitador]\n[números]`.
   Ex.: `add("//;\n1;2")` retorna `3`.
6. Se a string contiver **números negativos**, a função deve lançar um erro cuja mensagem contenha o(s) número(s) negativo(s) informado(s).
   Ex.: `add("1,-2,3")` deve lançar um erro contendo `"-2"`.

### Exemplos

```js
add("");          // 0
add("1");         // 1
add("1,2");       // 3
add("1,2,3,4,5"); // 15
add("1\n2,3");    // 6
add("//;\n1;2");  // 3
add("1,-2,3");    // lança erro contendo "-2"
```
