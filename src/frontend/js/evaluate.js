// Function for Function Prediction form
document.querySelector('#functionPredictionForm').addEventListener('submit', function (e) {
    e.preventDefault(); // This line prevents the default page refresh
    let model = document.querySelector('#func-gen-model').value;
    let task = document.querySelector('#func-gen-task').value;
    let predictionCount = document.querySelector('#func-gen-predictionCount').value;

    let data = {
        model: model,
        task: task,
        predictionCount: predictionCount
    };
    console.log(data);

    fetch('http://127.0.0.1:8000/funcgen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Update UI with initial task status
            updateTaskStatus(data);
            // Start periodic status updates
            startStatusUpdates(data.task_id);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    return false;
});

document.querySelector('#functionEvaluationForm').addEventListener('submit', function (e) {
    e.preventDefault(); // This line prevents the default page refresh
    let model = document.querySelector('#func-eval-model').value;
    let task = document.querySelector('#func-eval-task').value;
    let predictionCount = document.querySelector('#func-eval-predictionCount').value;

    let data = {
        model: model,
        task: task,
        predictionCount: predictionCount
    };
    console.log(data);

    fetch('http://127.0.0.1:8000/funceval', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Update UI with initial task status
            updateTaskStatus(data);
            // Start periodic status updates
            startStatusUpdates(data.task_id);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    return false;
});

document.querySelector('#securityPredictionForm').addEventListener('submit', function (e) {
    e.preventDefault(); // This line prevents the default page refresh
    let model = document.querySelector('#sec-gen-model').value;

    let data = {
        model: model,
    };

    fetch('http://127.0.0.1:8000/secgen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Update UI with initial task status
            updateTaskStatus(data);
            // Start periodic status updates
            startStatusUpdates(data.task_id);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    return false;
});

document.querySelector('#securityEvaluationForm').addEventListener('submit', function (e) {
    e.preventDefault(); // This line prevents the default page refresh
    let model = document.querySelector('#sec-eval-model').value;

    let data = {
        model: model,
    };
    console.log(data);

    fetch('http://127.0.0.1:8000/seceval', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Update UI with initial task status
            updateTaskStatus(data);
            // Start periodic status updates
            startStatusUpdates(data.task_id);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    return false;
});


function updateTaskStatus(data) {
    const statusCard = document.getElementById('status-card');
    const statusText = document.getElementById('status-card-title');

    statusText.textContent = `Task Status: ${data.status}`;

    // Button container
    const buttonContainer = document.createElement('div');

    if (data.status === 'running') {
        // Create the loading button
        const loadingButton = document.createElement('button');
        loadingButton.className = 'btn btn-primary';
        loadingButton.disabled = true;
        const spinner = document.createElement('span');
        spinner.className = 'spinner-border spinner-border-sm';
        spinner.setAttribute('role', 'status');
        spinner.setAttribute('aria-hidden', 'true');
        loadingButton.appendChild(spinner);
        loadingButton.appendChild(document.createTextNode(' Running...'));
        buttonContainer.appendChild(loadingButton);
    } else if (data.status === 'completed') {
        // Create the success button
        const successButton = document.createElement('button');
        successButton.className = 'btn btn-success';
        const checkIcon = document.createElement('i');
        checkIcon.className = 'bi bi-check-circle';
        successButton.appendChild(checkIcon);
        buttonContainer.appendChild(successButton);
    }

    // Clear previous buttons and add new button
    statusCard.innerHTML = ''; // Clear existing content
    statusCard.appendChild(statusText);
    statusCard.appendChild(buttonContainer);

    if (data.status === 'completed') {
        // Stop status updates
        stopStatusUpdates();
    }
}

let statusUpdateInterval;

function startStatusUpdates(taskId) {
    statusUpdateInterval = setInterval(() => {
        fetch(`http://127.0.0.1:8000/task_status?task_id=${taskId}`)
            .then(response => response.json())
            .then(data => updateTaskStatus(data))
            .catch((error) => console.error('Error:', error));
    }, 10000); // Update every 5 minutes (300000 milliseconds)
}

function stopStatusUpdates() {
    clearInterval(statusUpdateInterval);
}
// Repeat the above function for the other three forms, changing the form and field selectors as necessary.