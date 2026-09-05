const form = document.getElementById("fileForm");

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const result = document.getElementById("result");

    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    result.classList.remove("hidden");

    document.getElementById("filename").innerHTML = "Checking...";
    document.getElementById("status").innerHTML = "Analyzing...";
    document.getElementById("risk").innerHTML = "...";

    try {

        const response = await fetch("/check", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("filename").innerHTML =
            data.filename;

        document.getElementById("status").innerHTML =
            `<span class="badge ${
                data.status === "FILE MODIFIED"
                ? "modified"
                : "verified"
            }">${data.status}</span>`;

        document.getElementById("risk").innerHTML =
            `<span class="badge ${data.risk.toLowerCase()}">
                ${data.risk}
            </span>`;

        document.getElementById("difference").innerHTML =
            data.difference;

        document.getElementById("differentBits").innerHTML =
            data.different_bits;

        document.getElementById("executionTime").innerHTML =
            data.execution_time;

        document.getElementById("originalHash").innerHTML =
            data.original_hash;

        document.getElementById("currentHash").innerHTML =
            data.current_hash;

        document.getElementById("aiAnalysis").innerHTML =
            data.ai_analysis ||
            "AI analysis not available for this check.";

        loadHistory();

    } catch (error) {

        console.error(error);

        alert("Something went wrong while checking the file.");
    }
});


/* LOAD HISTORY */

async function loadHistory() {

    const historyTable =
        document.getElementById("historyTable");

    try {

        const response = await fetch("/history");

        const data = await response.json();

        historyTable.innerHTML = "";

        if (data.length === 0) {

            historyTable.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align:center;">
                        No verification history found.
                    </td>
                </tr>
            `;

            return;
        }

        data.forEach(function(record) {

            const row = document.createElement("tr");

            const statusClass =
                record.status === "FILE MODIFIED"
                ? "modified"
                : "verified";

            const riskClass =
                record.risk.toLowerCase();

            row.innerHTML = `

                <td>${record.filename}</td>

                <td>
                    <span class="badge ${statusClass}">
                        ${record.status}
                    </span>
                </td>

                <td>
                    <span class="badge ${riskClass}">
                        ${record.risk}
                    </span>
                </td>

                <td>
                    ${record.difference}%
                </td>

                <td>
                    ${record.execution_time}s
                </td>

                <td>
                    ${record.checked_at}
                </td>

                <td>
                    <button
                        class="delete-button"
                        onclick="deleteRecord(${record.id})">
                        🗑️
                    </button>
                </td>

            `;

            historyTable.appendChild(row);

        });

    } catch (error) {

        console.error(error);

    }
}


/* LOAD HISTORY BUTTON */

document
    .getElementById("historyButton")
    .addEventListener("click", loadHistory);


/* DELETE ONE RECORD */

async function deleteRecord(id) {

    const confirmDelete =
        confirm("Delete this verification record?");

    if (!confirmDelete) {
        return;
    }

    await fetch(`/history/delete/${id}`, {
        method: "DELETE"
    });

    loadHistory();
}


/* CLEAR ALL HISTORY */

document
    .getElementById("clearHistoryButton")
    .addEventListener("click", async function() {

        const confirmClear =
            confirm(
                "Clear all verification history?\n\n" +
                "Original file hashes will NOT be deleted."
            );

        if (!confirmClear) {
            return;
        }

        await fetch("/history/clear", {
            method: "DELETE"
        });

        loadHistory();

    });