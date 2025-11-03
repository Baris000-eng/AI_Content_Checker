// background.js - Listen for the extension being installed or the popup being opened
chrome.runtime.onInstalled.addListener(() => {
    console.log("AI Content Detector Extension Installed!");
});

// Example of messaging with content scripts or popup
chrome.runtime.onConnect.addListener((port) => {
    console.log('Connected to port:', port);
    port.postMessage({ greeting: "Hello from Background!" });
});

// Example of opening the popup and doing some work in the background
chrome.action.onClicked.addListener((tab) => {
    console.log("AI Content Detector Extension Icon Clicked!");
    // Open the popup or do something when the icon is clicked
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
            alert("The AI Content Detector is active!");
        }
    });
});
