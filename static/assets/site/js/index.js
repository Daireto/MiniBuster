const randomValue = () => {
    return Math.max.apply(null, [70,80,90,100]) * Math.random();
}

$(document).ready(async () => {
    const resources = await get('/maintenance/get_resources');
    createGauge('cpu', resources['cpu']);
    createGauge('memory', resources['memory']);
    createGauge('disk', resources['disk']);
    // TODO: Refresh data with setInterval
});
