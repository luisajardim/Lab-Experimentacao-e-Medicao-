# Kata 02 — Roman Numerals

## Enunciado

Implemente a função `toRoman(num)` que converte um número inteiro (de `1` a `3999`) para sua representação em **algarismos romanos** (string).

### Tabela de referência

| Símbolo | Valor |
| :-----: | :---: |
|    I    |   1   |
|    V    |   5   |
|    X    |   10  |
|    L    |   50  |
|    C    |  100  |
|    D    |  500  |
|    M    |  1000 |

### Regras de formação

- Símbolos são somados quando escritos em ordem decrescente (ex.: `VI` = 6).
- Um símbolo menor colocado **antes** de um maior é subtraído (ex.: `IV` = 4, `IX` = 9, `XL` = 40, `XC` = 90, `CD` = 400, `CM` = 900).
- Não é permitido repetir um mesmo símbolo mais de 3 vezes seguidas.

### Exemplos

```js
toRoman(3);    // "III"
toRoman(4);    // "IV"
toRoman(9);    // "IX"
toRoman(58);   // "LVIII"
toRoman(1994); // "MCMXCIV"
```

### Regras adicionais

- Se `num` for menor que `1`, maior que `3999`, ou não for um número inteiro, a função deve lançar um erro (`throw`).
