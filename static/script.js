// 1️⃣ File input listener: fills textarea when a file is selected
const fileInput = document.getElementById("fileInput");
const textarea = document.getElementById("content");

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;

  const ext = file.name.split(".").pop().toLowerCase();

  if (ext === "txt") {
    const reader = new FileReader();
    reader.onload = (e) => {
      textarea.value = e.target.result;
    };
    reader.readAsText(file);
  } else {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/extract-text", {
        method: "POST",
        body: formData
      });
      const data = await response.json();
      if (data.error) {
        textarea.value = `Error extracting text: ${data.error}`;
      } else {
        textarea.value = data.text;
      }
    } catch (err) {
      textarea.value = `Error: ${err.message}`;
    }
  }
});

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
    const response = await fetch("/predict", { 
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Failed to get response");
    }

    // Parse the response JSON
    const data = await response.json();

    // Check for errors in the response
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

      let chunkText = item.chunk;

      // Highlight AI-generated content
      if (item.ai_prob > item.human_prob) {
        chunkText = `<span class="highlight-ai">${chunkText}</span>`;
      } else {
        chunkText = `<span class="highlight-human">${chunkText}</span>`;
      }

      chunkDiv.innerHTML = `
        <p>${chunkText}</p>
        <p><strong>AI Generated Probability:</strong> ${item.ai_prob.toFixed(2)}%</p>
        <p><strong>Human Written Probability:</strong> ${item.human_prob.toFixed(2)}%</p>
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
