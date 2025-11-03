document.getElementById("checkBtn").addEventListener("click", async () => {
    const text = document.getElementById("content").value.trim();
    const fileInput = document.getElementById("fileInput");
    const resultDiv = document.getElementById("result");

    // Clear previous result
    resultDiv.innerHTML = "";
    resultDiv.className = "";  
    
    // Validate input
    if (!text && fileInput.files.length === 0) {
        resultDiv.innerText = "Please enter some text or upload a file!";
        resultDiv.className = "error";
        return;
    }

    resultDiv.innerText = "Checking...";

    const formData = new FormData();
    formData.append("text", text);
    if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
    }

    try {
        // Make the POST request to the Flask backend
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        // Check if the response is OK
        if (!response.ok) {
            resultDiv.innerText = "Error: Unable to process your request.";
            resultDiv.className = "error";
            return;  // Stop further execution if the response isn't OK
        }

        // Parse the response JSON
        const data = await response.json();

        // Check for errors in the response data
        if (data.error) {
            resultDiv.innerText = "Error: " + data.error;
            resultDiv.className = "error";
            return;
        }

        // Clear the result div
        resultDiv.innerHTML = '';

        // Iterate through the chunks and display them with highlights and probabilities
        data.forEach(item => {
            const chunkDiv = document.createElement("div");

            // Create a span element for the chunk of text
            let chunkText = item.chunk;

            // Highlight AI-generated content
            if (item.ai_prob > item.human_prob) {
                // Apply highlighting for AI-generated content
                chunkText = `<span class="highlight-ai">${chunkText}</span>`;
            } else {
                // Apply highlighting for Human-generated content
                chunkText = `<span class="highlight-human">${chunkText}</span>`;
            }

            // Add the chunk text with AI-generated probability
            chunkDiv.innerHTML = `
                <p>${chunkText}</p>
                <p><strong>AI Generated Probability:</strong> ${item.ai_prob}%</p>
                <p><strong>Human Written Probability:</strong> ${item.human_prob}%</p>
            `;

            // Append the chunk div to the result div
            resultDiv.appendChild(chunkDiv);
        });

        resultDiv.className = "success";  // Add success styling

    } catch (err) {
        resultDiv.innerText = "Error: " + err.message;
        resultDiv.className = "error";
    }
});
