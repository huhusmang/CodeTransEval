async function fetchData() {
    const response = await fetch('http://127.0.0.1:8000/results');
    return response.json();
}

function populateSelectOptions(data) {
    const modelSelect = document.getElementById('model-select');

    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item.model;
        option.textContent = item.model;
        modelSelect.appendChild(option);
    });
}

var chart = echarts.init(document.getElementById('testChart'));

function initChart() {
    var option = {
        title: {
            text: 'Model and Task Performance'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['Pass@1 rate', 'CodeBLEU']
        },
        grid: {
            left: '3%',
            right: '3%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: true,
            data: [], // to be filled based on selection
            axisLabel: {
                interval: 0, // Display all labels without auto interval
                rotate: 45, // Rotate labels to fit
                fontSize: 13 // Smaller font size to prevent overlap
            },
            axisTick: {
                show: false // This will hide the axis tick lines
            },
            axisLine: {
                show: false // This will hide the axis line
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                fontSize: 12
            }
        },
        series: [
            {
                name: 'Pass@1 rate',
                type: 'bar',
                data: []
            },
            {
                name: 'CodeBLEU',
                type: 'bar',
                data: []
            }
        ]
    };
    chart.setOption(option);
}


function updateVisualization(data, selectedModel, selectedTask) {
    let xAxisData = [];
    let passRateData = [];
    let codebleuData = [];

    data.forEach(model => {
        model.tasks_results.forEach(task => {
            if ((selectedModel === 'all' || model.model === selectedModel) &&
                (selectedTask === 'all' || task.task === selectedTask)) {
                let taskLabel = `${model.model} - ${task.task}`;
                xAxisData.push(taskLabel);
                passRateData.push(task.result['Pass@1 rate']);
                codebleuData.push(task.result.CodeBLEU.codebleu);
            }
        });
    });

    chart.setOption({
        xAxis: {
            data: xAxisData
        },
        series: [
            {
                name: 'Pass@1 rate',
                data: passRateData
            },
            {
                name: 'CodeBLEU',
                data: codebleuData
            }
        ]
    });
}


document.addEventListener('DOMContentLoaded', async () => {
    const data = await fetchData();
    populateSelectOptions(data);
    initChart(); // Initialize the chart with no data

    const modelSelect = document.getElementById('model-select');
    const taskSelect = document.getElementById('task-select');

    modelSelect.addEventListener('change', () => {
        updateVisualization(data, modelSelect.value, taskSelect.value);
    });

    taskSelect.addEventListener('change', () => {
        updateVisualization(data, modelSelect.value, taskSelect.value);
    });
});

