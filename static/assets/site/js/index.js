const randomValue = () => {
    return Math.max.apply(null, [70,80,90,100]) * Math.random();
}

$(document).ready(async () => {
    const resources = await get('/maintenance/get_resources');
    createGauge('cpu', resources['cpu']);
    createGauge('memory', resources['memory']);
    createGauge('disk', resources['disk']);
    setInterval(async () => {
        const resources = await get('/maintenance/get_resources');
        updateGauge('cpu', resources['cpu']);
        updateGauge('memory', resources['memory']);
        updateGauge('disk', resources['disk']);
    }, 1000);
});
