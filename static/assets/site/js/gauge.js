const getMetrics = () => {
    return {
        normal: {
            value: 70,
            color: 'green'
        },
        warning: {
            value: 80,
            color: 'yellow'
        },
        danger: {
            value: 90,
            color: 'orange'
        },
        panic: {
            value: 100,
            color: 'red'
        },
    }
}

const getGaugeData = () => {
    const data = [];
    const colors = [];
    const metrics = getMetrics();
    for(const metric in metrics) {
        data.push(metrics[metric].value);
        colors.push(metrics[metric].color);
    }
    return {data: data, colors: colors}
}

const getGaugeConfig = (value, darkMode) => {
    const chartConfig = getGaugeData()
    return {
        type: 'gauge',
        data: {
            datasets: [{
                data: chartConfig.data,
                value: value,
                backgroundColor: chartConfig.colors,
                borderColor: darkMode ? 'rgba(255, 255, 255, 1)': 'rgba(0, 0, 0, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            layout: {
                padding: {
                    bottom: 30
                }
            },
            needle: {
                radiusPercentage: 2,
                widthPercentage: 3.2,
                lengthPercentage: 80,
                color: darkMode ? 'rgb(142, 141, 142)': 'rgba(0, 0, 0, 1)'
            },
            valueLabel: {
                formatter: (value) => {
                    return `${Math.round(value)}%`;
                },
                fontSize: 16,
                color: 'rgba(255, 255, 255, 1)',
                backgroundColor: darkMode ? 'rgb(142, 141, 142)': 'rgba(0, 0, 0, 1)',
                borderRadius: 5,
                padding: {
                    top: 5,
                    right: 5,
                    bottom: 5,
                    left: 5
                }
            }
        }
    };
}

const createGauge = (source, value = 0) => {
    const gaugeConfig = getGaugeConfig(value, window.darkMode);
    const ctx = $(`#${source}-gauge`)[0].getContext('2d');
    window[`${source}Gauge`] = new Chart(ctx, gaugeConfig);
}

const updateGauge = (source, value = 0) => {
    const chart = window[`${source}Gauge`];
    chart.data.datasets[0].value = value;
    chart.update();
}
