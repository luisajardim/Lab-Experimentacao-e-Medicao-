# Prompts Utilizados no Trial

**Dev:** luisajardim | **Kata:** kata-02-roman-numerals | **Tratamento:** COM_IA

---

## Prompt 1

> Implemente a função `toRoman(num)` que converte um número inteiro (de 1 a 3999) para sua representação em algarismos romanos (string).
>
> Tabela de referência: I=1, V=5, X=10, L=50, C=100, D=500, M=1000.
>
> Regras de formação: símbolos são somados quando escritos em ordem decrescente (ex.: VI = 6). Um símbolo menor colocado antes de um maior é subtraído (ex.: IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900). Não é permitido repetir um mesmo símbolo mais de 3 vezes seguidas.
>
> Exemplos: toRoman(3) = "III", toRoman(4) = "IV", toRoman(9) = "IX", toRoman(58) = "LVIII", toRoman(1994) = "MCMXCIV".
>
> Regra adicional: se num for menor que 1, maior que 3999, ou não for um número inteiro, a função deve lançar um erro (throw).

**Resposta da IA:**

```js
const VALUES = [
  [1000, "M"],
  [900, "CM"],
  [500, "D"],
  [400, "CD"],
  [100, "C"],
  [90, "XC"],
  [50, "L"],
  [40, "XL"],
  [10, "X"],
  [9, "IX"],
  [5, "V"],
  [4, "IV"],
  [1, "I"],
];

function toRoman(num) {
  if (typeof num !== "number" || !Number.isInteger(num) || num < 1 || num > 3999) {
    throw new RangeError("num must be an integer between 1 and 3999");
  }

  let remaining = num;
  let result = "";
  for (const [value, symbol] of VALUES) {
    while (remaining >= value) {
      result += symbol;
      remaining -= value;
    }
  }
  return result;
}

module.exports = { toRoman };
```

A estratégia é a clássica "greedy": percorrer os valores em ordem decrescente (incluindo os pares de subtração como 900/CM, 400/CD etc.) e ir subtraindo enquanto o valor couber no restante. Isso já respeita a regra de não repetir símbolos mais de 3 vezes, pois os pares de subtração (IV, IX, XL, XC, CD, CM) evitam sequências como "IIII" ou "VIIII".

Solução aplicada diretamente, sem necessidade de prompts de correção — a suíte de aceite passou de primeira (26/26 testes, `test_attempts: 1`).
