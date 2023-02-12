const randomValue = () => {
    return Math.max.apply(null, [70,80,90,100]) * Math.random();
}

$(document).ready(() => {
    createGauge('cpu', randomValue());
    createGauge('memory', randomValue());
    createGauge('disk', randomValue());
});
