let currentPage = 0;
let ITEMS_PER_PAGE = 20;
let NUM_PAGES = 5;
let url = ``;


$('#predictionForm').submit(function (event) {
    event.preventDefault(); // Prevent default form submission

    const selectedModel = encodeURIComponent($('#optional-model').val());
    const selectedTask = encodeURIComponent($('#optional-task').val());
    // 使用 get 传参
    url = `http://127.0.0.1:8000/predict?model=${selectedModel}&task=${selectedTask}`;

    loadData();
});

window.onload = function () {

    document.getElementById("prev-btn").addEventListener("click", () => handlePageChange("prev"));
    document.getElementById("next-btn").addEventListener("click", () => handlePageChange("next"));

    // Export buttons
    // document.getElementById("export-func-btn").addEventListener("click", () => exportData("function"));

};


function loadData() {
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            // Update page buttons based on the (potentially filtered) data
            generatePageButtons(data);

            // Apply pagination
            const startIndex = currentPage * ITEMS_PER_PAGE;
            const endIndex = startIndex + ITEMS_PER_PAGE;
            const paginatedData = data.slice(startIndex, endIndex);

            populateTable(paginatedData); // Update the table
        })
        .catch((error) => console.error("Error:", error));
}


function generatePageButtons(data) {
    const totalQuestions = data.length;
    const numPages = Math.ceil(totalQuestions / ITEMS_PER_PAGE);

    const pageButtonsDiv = document.getElementById(`page-buttons`); //TODO
    pageButtonsDiv.innerHTML = ""; // Clear existing buttons

    for (let i = 1; i <= numPages; i++) {
        const btn = document.createElement("button");
        btn.textContent = i;
        btn.addEventListener("click", () => {
            currentPage = i - 1;
            loadData();
        });
        pageButtonsDiv.appendChild(btn);
    }
}

function handlePageChange(direction) {
    if (direction === "prev" && currentPage > 0) {
        currentPage--;
    } else if (direction === "next" && currentPage < NUM_PAGES - 1) {
        currentPage++;
    }
    loadData(); // Reload data for the new page
}


function populateTable(data) {
    const tableBody = document.querySelector(`#data-table tbody`); //TODO
    tableBody.innerHTML = ""; // Clear existing data

    data.forEach((row) => {
        const tableRow = document.createElement("tr");

        // Create cells for all columns
        const idCell = document.createElement("td");
        idCell.textContent = row.problem_id;
        tableRow.appendChild(idCell);

        // Create cells for Params, Python, Java, and C++ with truncation
        const rawPredictionCell = document.createElement("td");
        rawPredictionCell.classList.add("truncated-cell");
        rawPredictionCell.textContent = JSON.stringify(row.raw_prediction);
        tableRow.appendChild(rawPredictionCell);

        const processPredictionCell = document.createElement("td");
        processPredictionCell.classList.add("truncated-cell");
        processPredictionCell.textContent = row.pro_prediction;
        tableRow.appendChild(processPredictionCell);

        const slGoldCodeCell = document.createElement("td");
        slGoldCodeCell.classList.add("truncated-cell");
        slGoldCodeCell.textContent = row.sl_gold_code;
        tableRow.appendChild(slGoldCodeCell);

        const tlGoldCodeCell = document.createElement("td");
        tlGoldCodeCell.classList.add("truncated-cell");
        tlGoldCodeCell.textContent = row.tl_gold_code;
        tableRow.appendChild(tlGoldCodeCell);

        // Add event listeners to expand cells on click
        rawPredictionCell.addEventListener("click", () => expandCells(tableRow));
        processPredictionCell.addEventListener("click", () => expandCells(tableRow));
        slGoldCodeCell.addEventListener("click", () => expandCells(tableRow));
        tlGoldCodeCell.addEventListener("click", () => expandCells(tableRow));

        tableBody.appendChild(tableRow);
    });
}

// Function to expand cells in a row
function expandCells(row) {
    row.querySelectorAll(".truncated-cell").forEach((cell) => {
        cell.classList.toggle("expanded"); // Toggle the "expanded" class
    });
}


function exportData() {
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], { type: "application/json" });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement("a");
            link.href = url;
            link.download = "data.json";
            link.click();
        })
        .catch((error) => console.error("Error:", error));
}