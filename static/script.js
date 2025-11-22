const fileInput = document.getElementById("fileInput");
const textarea = document.getElementById("content");
const resultDiv = document.getElementById("result");
const checkBtn = document.getElementById("checkBtn");

let fileContent = ""; // Store file content

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;

  resultDiv.innerHTML = "";  // Clear previous prediction content

  // Display the loading message
  textarea.value = "Loading document content...";  
  textarea.disabled = true;  // Disable the textarea to prevent editing while loading

  const ext = file.name.split(".").pop().toLowerCase();

  // Clear textarea before processing new file
  if (ext === "txt") {
    // For .txt files, load the content via FileReader
    const reader = new FileReader();
    reader.onload = (e) => {
      fileContent = e.target.result;
      textarea.value = fileContent;  // Display content in textarea
      textarea.disabled = false;  // Re-enable textarea after content is loaded
    };
    reader.readAsText(file);  // Read the file as text
  } else {
    // For non-text files, send them for processing
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/extract-text-from-file-or-plain-text", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (data.error) {
        textarea.value = `Error extracting text: ${data.error}`;
      } else {
        fileContent = data.text;
        textarea.value = fileContent;
      }
      textarea.disabled = false;  // Re-enable textarea after content is loaded
    } catch (err) {
      textarea.value = `Error: ${err.message}`;
      textarea.disabled = false;  // Re-enable textarea in case of error
    }
  }
});

// When the "Check" button is clicked, send the content for prediction
checkBtn.addEventListener("click", async () => {
  const text = textarea.value.trim();
  resultDiv.innerHTML = "";  // Clear previous result

  if (!text) {
    resultDiv.innerText = "Please enter some text or upload a file!";
    resultDiv.className = "error";
    return;
  }

  resultDiv.innerText = "Checking...";  // Show loading message

  const formData = new FormData();
  formData.append("text", text);  // Append the text from the textarea

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Failed to get response from the server");
    }

    const data = await response.json();

    // Check for errors in the response
    if (data.error) {
      resultDiv.innerText = `Error: ${data.error}`;
      resultDiv.className = "error";
      return;
    }

    // Clear the previous results
    resultDiv.innerHTML = "";

    // Display the results for each chunk
    data.forEach(item => {
      const chunkDiv = document.createElement("div");
      let chunkText = item.chunk;

      // Highlight AI-generated content vs. human-written
      if (item.ai_prob > item.human_prob) {
        chunkText = `<span class="highlight-ai">${chunkText}</span>`;
      } else {
        chunkText = `<span class="highlight-human">${chunkText}</span>`;
      }

      chunkDiv.innerHTML = `
        <p>${chunkText}</p>
        <p>AI Generated Probability: ${(item.ai_prob * 100)}%</p>
        <p>Human Written Probability: ${(item.human_prob * 100)}%</p>
      `;

      resultDiv.appendChild(chunkDiv);
    });

    resultDiv.className = "success";  // Add success styling

  } catch (err) {
    resultDiv.innerText = `Error: ${err.message}`;
    resultDiv.className = "error";
  }
});
