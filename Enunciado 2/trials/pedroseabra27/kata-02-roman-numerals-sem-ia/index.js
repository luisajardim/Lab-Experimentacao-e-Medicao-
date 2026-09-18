function toRoman(num) {
  if (!Number.isInteger(num) || num < 1 || num > 3999) {
    throw new Error("o numero tem que ser inteiro e maior que 1 e menor que 3999");

  }

  const romanos = [
    { valor: 1000, chave: 'M' },
    { valor: 900, chave: 'CM' },
    { valor: 500, chave: 'D' },
    { valor: 400, chave: 'CD' },
    { valor: 100, chave: 'C' },
    { valor: 90, chave: 'XC' },
    { valor: 50, chave: 'L' },
    { valor: 40, chave: 'XL' },
    { valor: 10, chave: 'X' },
    { valor: 9, chave: 'IX' },
    { valor: 5, chave: 'V' },
    { valor: 4, chave: 'IV' },
    { valor: 1, chave: 'I' }

  ]
  let Resultado = "";

  for (let rom of romanos) {
    while (num >= rom.valor) {
      Resultado += rom.chave
      num -= rom.valor
    }
  }


  return Resultado;
}

module.exports = { toRoman };
