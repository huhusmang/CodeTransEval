async function fetchResults() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/results');
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function updateTable() {
    const task = document.getElementById('task-select').value;
    const data = await fetchResults();
    const tbody = document.querySelector('#leaaderboard-data-table tbody');
    tbody.innerHTML = ''; // Clear existing table data
    data.forEach((model, index) => {
        model.tasks_results.forEach(taskResult => {
            if (taskResult.task === task) {
                const row = `<tr>
                            <td>${model.model}</td>
                            <td>${parseFloat(taskResult.result['Pass@1 rate']).toFixed(2)}</td>
                            <td>${parseFloat(taskResult.result.CodeBLEU.codebleu).toFixed(2)}</td>
                        </tr>`;
                tbody.innerHTML += row;
            }
        });
    });
}

function sortTable(column) {
    const table = document.getElementById("leaaderboard-data-table");
    const tbody = document.querySelector('#leaaderboard-data-table tbody');
    let rows = Array.from(tbody.querySelectorAll("tr"));
    let isAscending = tbody.getAttribute("data-sort-order") === "asc";
    rows.sort((a, b) => {
        const aColText = a.children[column].textContent.trim();
        const bColText = b.children[column].textContent.trim();
        const aColVal = isNaN(aColText) ? aColText.toLowerCase() : parseFloat(aColText);
        const bColVal = isNaN(bColText) ? bColText.toLowerCase() : parseFloat(bColText);
        return aColVal > bColVal ? (isAscending ? 1 : -1) : (isAscending ? -1 : 1);
    });
    tbody.innerHTML = "";  // Clear current rows
    rows.forEach(row => tbody.appendChild(row));
    tbody.setAttribute("data-sort-order", isAscending ? "desc" : "asc");  // Toggle sort order
    updateArrows(column, isAscending);
}

function updateArrows(selectedColumn, isAscending) {
    for (let i = 0; i < 3; i++) {
        const arrowSpan = document.getElementById(`arrow${i}`);
        if (i === selectedColumn) {
            arrowSpan.textContent = isAscending ? ' ↑' : ' ↓';
        } else {
            arrowSpan.textContent = '';
        }
    }
}


document.addEventListener('DOMContentLoaded', updateTable); // This ensures the script runs after the page has fully loaded