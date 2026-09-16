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
