function isValidISBN10(isbn) {
  if (typeof isbn !== 'string' || isbn.length <= 0) return false;
  let sum = 0;
  for (let index = 0; index < isbn.length; index++) {
    const element = isbn[index];
    if (index !== isbn.length - 1 && Number.isNaN(element)) return false;
    if (index === isbn.length - 1 && (Number.isNaN(element) && element !== 'X')) return false;
    sum += (element === 'X' ? 10 : Number(element)) * (10 - index); 
  }
  return sum % 11 === 0 ? true : false;
}

module.exports = { isValidISBN10 };
