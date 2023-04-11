let weatherCondition = '{{ weather.condition }}';
let body = document.querySelector('body');

if (weatherCondition === 'Sunny') {
    body.classList.add('sun');
} else if (weatherCondition === 'Rainy') {
    body.classList.add('rain');
}
