# Prompts Utilizados no Trial

**Dev:** luisajardim | **Kata:** kata-03-string-calculator | **Tratamento:** COM_IA

---

## Prompt 1

> Implemente a função `add(numbers)` que recebe uma string de números separados por delimitadores e retorna a soma desses números. Regras (todas devem ser suportadas simultaneamente):
> 1. Aceita string vazia e retorna 0.
> 2. Aceita 1 ou 2 números separados por vírgula.
> 3. Aceita quantidade qualquer de números separados por vírgula.
> 4. Aceita quebras de linha (\n) além de vírgulas como delimitadores.
> 5. Aceita um delimitador customizado, informado na primeira linha no formato `//[delimitador]\n[números]`.
> 6. Se a string contiver números negativos, lança um erro cuja mensagem contenha o(s) número(s) negativo(s) informado(s).
>
> Exemplos: add("") = 0, add("1,2") = 3, add("1,2,3,4,5") = 15, add("1\n2,3") = 6, add("//;\n1;2") = 3, add("1,-2,3") lança erro contendo "-2".

**Resposta da IA:**

```js
function add(numbers) {
  if (numbers === "") return 0;

  let delimiter = /,|\n/;
  let body = numbers;

  if (numbers.startsWith("//")) {
    const newlineIndex = numbers.indexOf("\n");
    const customDelimiter = numbers.slice(2, newlineIndex);
    delimiter = new RegExp(customDelimiter.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    body = numbers.slice(newlineIndex + 1);
  }

  const nums = body
    .split(delimiter)
    .map((value) => value.trim())
    .filter((value) => value.length > 0)
    .map(Number);

  const negatives = nums.filter((value) => value < 0);
  if (negatives.length > 0) {
    throw new Error(`negatives not allowed: ${negatives.join(", ")}`);
  }

  return nums.reduce((sum, value) => sum + value, 0);
}

module.exports = { add };
```

Abordagem: por padrão o delimitador é vírgula ou quebra de linha (`/,|\n/`). Se a string começar com `//`, extrai o delimitador customizado da primeira linha (escapando caracteres especiais de regex) e usa o restante da string como corpo. Depois faz split, converte pra número, filtra negativos (lançando erro com a lista deles) e soma o restante com `reduce`.

Solução aplicada diretamente, sem necessidade de prompts de correção — a suíte de aceite passou de primeira (15/15 testes, `test_attempts: 1`).
