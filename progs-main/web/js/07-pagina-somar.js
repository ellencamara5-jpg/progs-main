// ---------------------------------
// recursos deste arquivo javascript
// ---------------------------------

const PI = 3.14159;

function somar(a, b) {
  return a + b;
}

function multiplicar(a, b) {
  return a * b;
}

// -----
// ações
// -----

// colocando o valor na tela
document.getElementById('mostrar_pi').textContent = PI;

// somando números
const resultado = somar(5, 10);
document.getElementById('mostrar_soma').textContent = resultado;

// a função multiplicar foi importada por padrão
const mult = multiplicar(5, 10);
document.getElementById('mostrar_mult').textContent = mult;