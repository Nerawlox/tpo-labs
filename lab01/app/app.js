const form = document.querySelector('#calculator');
const first = document.querySelector('#first');
const second = document.querySelector('#second');
const operation = document.querySelector('#operation');
const output = document.querySelector('#output');

function readNumber(value) {
  const normalized = value.trim().replace(',', '.');
  if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(normalized)) {
    throw new Error('Введите два корректных числа');
  }
  const number = Number(normalized);
  if (!Number.isFinite(number)) throw new Error('Число вне допустимого диапазона');
  return number;
}

form.addEventListener('submit', event => {
  event.preventDefault();
  output.className = 'result';
  try {
    const a = readNumber(first.value), b = readNumber(second.value);
    if (operation.value === 'divide' && b === 0) throw new Error('Деление на ноль невозможно');
    const result = {add: () => a+b, subtract: () => a-b, multiply: () => a*b, divide: () => a/b}[operation.value]();
    if (!Number.isFinite(result)) throw new Error('Результат вне допустимого диапазона');
    output.replaceChildren();
    const label = document.createElement('div'); label.className = 'hint'; label.textContent = 'Результат';
    const number = document.createElement('strong'); number.id = 'result'; number.textContent = String(Number(result.toPrecision(12)));
    output.append(label, number);
  } catch (error) {
    output.classList.add('error-box'); output.textContent = error.message;
  }
});
document.querySelector('#clear').addEventListener('click', () => {
  form.reset(); output.className = 'result'; output.textContent = 'Результат появится после вычисления'; first.focus();
});
