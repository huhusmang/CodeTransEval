const ITEMS_PER_PAGE = {
    function: 20,
    security: 25,
};

const NUM_PAGES = {
    function: 5,
    security: 2,
};

let currentPage = {
    function: 0,
    security: 0,
};

let currentFilter = {
    function: null,
    security: null,
};

window.onload = function () {
    loadData("function"); // Load initial function data
    loadData("security"); // Load initial security data

    // Pagination buttons (previous and next)
    document.getElementById("function-prev-btn").addEventListener("click", () => handlePageChange("function", "prev"));
    document.getElementById("function-next-btn").addEventListener("click", () => handlePageChange("function", "next"));

    document.getElementById("security-prev-btn").addEventListener("click", () => handlePageChange("security", "prev"));
    document.getElementById("security-next-btn").addEventListener("click", () => handlePageChange("security", "next"));

    // Filter buttons
    document.getElementById("filter-easy-btn").addEventListener("click", () => filterData("function", "easy"));
    document.getElementById("filter-medium-btn").addEventListener("click", () => filterData("function", "medium"));
    document.getElementById("filter-hard-btn").addEventListener("click", () => filterData("function", "hard"));
    document.getElementById("filter-all-func-btn").addEventListener("click", () => filterData("function", "all"));

    document.getElementById("filter-top25-btn").addEventListener("click", () => filterData("security", true));
    document.getElementById("filter-all-sec-btn").addEventListener("click", () => filterData("security", "all"));

    // Export buttons
    document.getElementById("export-func-btn").addEventListener("click", () => exportData("function"));
    document.getElementById("export-sec-btn").addEventListener("click", () => exportData("security"));
};

// Function to handle page changes (both prev and next buttons)
function handlePageChange(dataType, direction) {
    if (direction === "prev" && currentPage[dataType] > 0) {
        currentPage[dataType]--;
    } else if (direction === "next" && currentPage[dataType] < NUM_PAGES[dataType] - 1) {
        currentPage[dataType]++;
    }
    loadData(dataType); // Reload data for the new page
}

// Function to load and update table data
function loadData(dataType) {
    const url = `http://127.0.0.1:8000/${dataType}data`;

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            // Filter data if a filter is applied and not "all"
            if (currentFilter[dataType] && currentFilter[dataType] !== "all") {
                data = data.filter((item) => {
                    if (dataType === "function") {
                        return item.difficulty === currentFilter[dataType];
                    } else if (dataType === "security") {
                        return item.Top25 === currentFilter[dataType];
                    }
                });
            }

            // Update page buttons based on the (potentially filtered) data
            generatePageButtons(dataType, data);

            // Apply pagination
            const startIndex = currentPage[dataType] * ITEMS_PER_PAGE[dataType];
            const endIndex = startIndex + ITEMS_PER_PAGE[dataType];
            const paginatedData = data.slice(startIndex, endIndex);

            populateTable(dataType, paginatedData); // Update the table
        })
        .catch((error) => console.error("Error:", error));
}

// Function to generate page buttons dynamically
function generatePageButtons(dataType, data) {
    const totalQuestions = data.length;
    const numPages = Math.ceil(totalQuestions / ITEMS_PER_PAGE[dataType]);

    const pageButtonsDiv = document.getElementById(`${dataType}-page-buttons`);
    pageButtonsDiv.innerHTML = ""; // Clear existing buttons

    for (let i = 1; i <= numPages; i++) {
        const btn = document.createElement("button");
        btn.textContent = i;
        btn.addEventListener("click", () => {
            currentPage[dataType] = i - 1;
            loadData(dataType);
        });
        pageButtonsDiv.appendChild(btn);
    }
}

// Function to filter data based on filter criteria
function filterData(dataType, filterValue) {
    currentFilter[dataType] = filterValue; // Store the current filter
    loadData(dataType); // Reload data with the applied filter
}

// Function to populate the table
function populateTable(dataType, data) {
    const tableBody = document.querySelector(`#${dataType}-data-table tbody`);
    tableBody.innerHTML = ""; // Clear existing data

    data.forEach((row) => {
        const tableRow = document.createElement("tr");

        // Create cells for all columns based on dataType
        if (dataType === "function") {
            // ... (Create and append cells for function data columns)
            // Create cells for all columns
            const idCell = document.createElement("td");
            idCell.textContent = row.id;
            tableRow.appendChild(idCell);

            const tagCell = document.createElement("td");
            tagCell.textContent = row.tag;
            tableRow.appendChild(tagCell);

            const difficultyCell = document.createElement("td");
            difficultyCell.textContent = row.difficulty;
            tableRow.appendChild(difficultyCell);

            const linkCell = document.createElement("td");
            const link = document.createElement("a");
            link.href = row.url;
            link.textContent = "Link";
            linkCell.appendChild(link);
            tableRow.appendChild(linkCell);

            const entryPointCell = document.createElement("td");
            entryPointCell.textContent = row.entry_point;
            tableRow.appendChild(entryPointCell);

            // Create cells for Params, Python, Java, and C++ with truncation
            const paramsCell = document.createElement("td");
            paramsCell.classList.add("truncated-cell");
            paramsCell.textContent = JSON.stringify(row.params);
            tableRow.appendChild(paramsCell);

            const pythonCell = document.createElement("td");
            pythonCell.classList.add("truncated-cell");
            pythonCell.textContent = row.python;
            tableRow.appendChild(pythonCell);

            const javaCell = document.createElement("td");
            javaCell.classList.add("truncated-cell");
            javaCell.textContent = row.java;
            tableRow.appendChild(javaCell);

            const cppCell = document.createElement("td");
            cppCell.classList.add("truncated-cell");
            cppCell.textContent = row.cpp;
            tableRow.appendChild(cppCell);

            // Add event listeners to expand cells on click
            paramsCell.addEventListener("click", () => expandCells(tableRow));
            pythonCell.addEventListener("click", () => expandCells(tableRow));
            javaCell.addEventListener("click", () => expandCells(tableRow));
            cppCell.addEventListener("click", () => expandCells(tableRow));
        } else if (dataType === "security") {
            // ... (Create and append cells for security data columns)
            // Create cells for all columns
            const idCell = document.createElement("td");
            idCell.textContent = row.ID;
            tableRow.appendChild(idCell);

            const descriptionCell = document.createElement("td");
            descriptionCell.classList.add("truncated-cell");
            descriptionCell.textContent = row.Description;
            tableRow.appendChild(descriptionCell);

            const vulCodeCell = document.createElement("td");
            vulCodeCell.classList.add("truncated-cell");
            vulCodeCell.textContent = row.VulCode;
            tableRow.appendChild(vulCodeCell);

            const sourceCell = document.createElement("td");
            const link = document.createElement("a");
            link.href = row.Source;
            link.textContent = "Link";
            sourceCell.appendChild(link);
            tableRow.appendChild(sourceCell);

            const top25Cell = document.createElement("td");
            top25Cell.textContent = row.Top25;
            tableRow.appendChild(top25Cell);

            descriptionCell.addEventListener("click", () => expandCells(tableRow));
            vulCodeCell.addEventListener("click", () => expandCells(tableRow));
        }

        tableBody.appendChild(tableRow);
    });
}

// Function to export current filtered data to a JSON file
function exportData(dataType) {
    const url = `http://127.0.0.1:8000/${dataType}data`;

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            // Filter data if a filter is applied and not "all"
            if (currentFilter[dataType] && currentFilter[dataType] !== "all") {
                data = data.filter((item) => {
                    if (dataType === "function") {
                        return item.difficulty === currentFilter[dataType];
                    } else if (dataType === "security") {
                        return item.Top25 === currentFilter[dataType];
                    }
                });
            }

            // Convert data to JSON and download it as a file
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

// Function to expand cells in a row
function expandCells(row) {
    row.querySelectorAll(".truncated-cell").forEach((cell) => {
        cell.classList.toggle("expanded"); // Toggle the "expanded" class
    });
}