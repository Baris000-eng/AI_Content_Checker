document.addEventListener("DOMContentLoaded", () => {
  // Get the HTML elements
  const textInput = document.getElementById("textInput");
  const analyzeButton = document.getElementById("analyzeButton");
  const resultDiv = document.getElementById("result");

  // Add a click listener to the button
  analyzeButton.addEventListener("click", () => {
    const text = textInput.value;

    if (text.trim() === "") {
      resultDiv.textContent = "Please enter text to analyze.";
      resultDiv.style.color = "red";
      return;
    }

    // Show a loading message
    resultDiv.textContent = "Analyzing...";
    resultDiv.style.color = "black";

    // Send the text to your Flask server
    fetch("http://localhost:5000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ "text_to_analyze": text }) 
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // Display the result from the server
      const scorePercent = (data.score * 100).toFixed(0);
      resultDiv.textContent = `Result: ${scorePercent} ${data.prediction}`;
      
      // Change color based on result
      if (data.prediction === "AI") {
        resultDiv.style.color = "red";
      } else {
        resultDiv.style.color = "green";
      }
    })
    .catch(error => {
      // Handle errors (like the server not running)
      console.error("Error:", error);
      resultDiv.textContent = "Analysis failed. (Is the server running?)";
      resultDiv.style.color = "red";
    });
  });
});