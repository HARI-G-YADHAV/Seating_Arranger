const authToken = localStorage.getItem('token');

// Check if the token exists
if (authToken) {
    // You can now use authToken for your authentication or other purposes
    console.log('Token:', authToken);

} 
else {
    console.log('Token not found in localStorage');
    window.location.href="http://127.0.0.1:5501/sign/notfound.html";

}

document.addEventListener("DOMContentLoaded", function () {
    const csvFileInput = document.getElementById("csvFileInput");
    const csvTable = document.getElementById("csvTable");

    csvFileInput.addEventListener("change", handleFileUpload);

    function handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.readAsText(file);
            reader.onload = function (e) {
                const csvData = e.target.result;
                const table = parseCSV(csvData);
                displayTable(table);
            };
        }
    }

    function parseCSV(csvData) {
        const lines = csvData.split("\n");
        const table = document.createElement("table");
    
        lines.forEach((line, index) => {
            if (line.trim() !== "") { // Check if the line is not empty
                const row = document.createElement(index === 0 ? "thead" : "tr");
                const cells = line.split(",");
                cells.forEach((cell, columnIndex) => {
                    const cellElement = index === 0 ? "th" : "td";
                    const cellNode = document.createElement(cellElement);
                    if (index === 0) {
                        // Set the column headers
                        if (columnIndex === 0) {
                            cellNode.textContent = "Status";
                        } else if (columnIndex === 1) {
                            cellNode.textContent = "Nominal Roll";
                        } else {
                            cellNode.textContent = cell;
                        }
                    } else {
                        cellNode.textContent = cell;
                    }
                    row.appendChild(cellNode);
                });
                table.appendChild(row);
            }
        });
    
        return table;
    }
    

    function displayTable(table) {
        csvTable.innerHTML = "";
        csvTable.appendChild(table);
    }
});




function uploadCsv() {
    const fileInput = document.getElementById('csvFileInput');
    const csvFile = fileInput.files[0];

    if (csvFile) {
        const formData = new FormData();
        formData.append('csv_file', csvFile);

        fetch('http://localhost:8000//api/upload-csv/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server (e.g., display a success message)
            console.log(data.message);
            // You can redirect the user to a success page if needed
            if (data.message === 'CSV file uploaded successfully') {
                window.location.href="upload_complete.html"
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle errors (e.g., display an error message)
        });
    } else {
        // Handle the case where no file is selected
        console.error('No CSV file selected');
    }
}
