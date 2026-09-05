const form = document.getElementById("fileForm");


form.addEventListener("submit", async function(event) {

    event.preventDefault();


    const fileInput =
        document.getElementById("fileInput");


    const result =
        document.getElementById("result");


    const file = fileInput.files[0];


    if (!file) {

        alert("Please select a file.");

        return;
    }


    const formData = new FormData();


    formData.append("file", file);


    result.classList.remove("hidden");


    result.innerHTML =
        "<h2>Checking file...</h2>";


    try {

        const response = await fetch("/check", {

            method: "POST",

            body: formData

        });


        const data = await response.json();


        if (data.error) {

            result.innerHTML =
                `<p>${data.error}</p>`;

            return;
        }


        // Restore result HTML

        result.innerHTML = `

            <h2>Security Analysis</h2>

            <p>
                <strong>File:</strong>
                <span id="filename"></span>
            </p>

            <p>
                <strong>Status:</strong>
                <span id="status"></span>
            </p>

            <p>
                <strong>Risk Level:</strong>
                <span id="risk"></span>
            </p>

            <p>
                <strong>Hash Difference:</strong>
                <span id="difference"></span>%
            </p>

            <p>
                <strong>Different Bits:</strong>
                <span id="differentBits"></span>
                / 256
            </p>

            <p>
                <strong>SHA-256 Execution Time:</strong>
                <span id="executionTime"></span>
                seconds
            </p>

            <div class="ai-box">

                <h3>AI Security Analysis</h3>

                <p id="aiAnalysis">
                Analyzing...
                </p>

            </div>
            

            <div class="hash-box">

                <strong>Original Hash:</strong>

                <p id="originalHash"></p>

            </div>

            <div class="hash-box">

                <strong>Current Hash:</strong>

                <p id="currentHash"></p>

            </div>

        `;


        // DOM manipulation

        document.getElementById("filename")
            .innerHTML = data.filename;


        document.getElementById("status")
            .innerHTML = data.status;


        document.getElementById("risk")
            .innerHTML = data.risk;


        document.getElementById("difference")
            .innerHTML = data.difference;


        document.getElementById("differentBits")
            .innerHTML = data.different_bits;


        document.getElementById("executionTime")
            .innerHTML = data.execution_time;

        document.getElementById("aiAnalysis")
            .innerHTML = data.ai_analysis;


        document.getElementById("originalHash")
            .innerHTML = data.original_hash;


        document.getElementById("currentHash")
            .innerHTML = data.current_hash;


    } catch (error) {

        result.innerHTML =
            "<p>Something went wrong.</p>";

        console.error(error);

    }

});


// History button

const historyButton =
    document.getElementById("historyButton");


historyButton.addEventListener("click", async function() {


    const historyDiv =
        document.getElementById("history");


    const response =
        await fetch("/history");


    const data =
        await response.json();


    historyDiv.innerHTML = "";


    data.forEach(function(record) {


        const item =
            document.createElement("div");


        item.classList.add("history-item");


        item.innerHTML = `

            <strong>${record.filename}</strong>

            <br>

            Status:
            ${record.status}

            <br>

            Risk:
            ${record.risk}

            <br>

            Hash Difference:
            ${record.difference}%

            <br>

            Checked:
            ${record.checked_at}

        `;


        historyDiv.appendChild(item);

    });

});