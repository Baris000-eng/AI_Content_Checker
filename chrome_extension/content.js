// let elements = Array.from(document.querySelectorAll("p"));
// let list = elements.map(p => p.innerText);

// // Send to background
// chrome.runtime.sendMessage({
//     type: "P_LIST",
//     list: list
// });

// // Handle validation results
// chrome.runtime.onMessage.addListener((msg) => {
//     if (msg.type === "VALIDATION_RESULT") {
//         let p = elements[msg.index];

//         if (!p) return;

//         if (msg.result === 1) {
//             p.style.border = "3px solid limegreen";
//             p.style.backgroundColor = "rgba(0,255,0,0.1)";
//         }
//         else if (msg.result === 2) {
//             p.style.border = "3px solid gold";
//             p.style.backgroundColor = "rgba(255,255,0,0.1)";
//         }
//         else if (msg.result === 3) {
//             p.style.border = "3px solid red";
//             p.style.backgroundColor = "rgba(255,0,0,0.1)";
//         }
//     }
// });


// let elements = Array.from(document.querySelectorAll("p"));
// let list = elements.map(p => p.innerText);

// // Send array to background
// chrome.runtime.sendMessage({
//     type: "P_LIST",
//     list: list
// });

// // Receive array of validity results
// chrome.runtime.onMessage.addListener((msg) => {
//     if (msg.type === "VALIDATION_RESULTS") {

//         let results = msg.results;

//         results.forEach((val, i) => {
//             let p = elements[i];
//             if (!p) return;

//             if (val === 1) {
//                 p.style.border = "3px solid limegreen";
//                 p.style.backgroundColor = "rgba(0,255,0,0.1)";
//             }
//             else if (val === 2) {
//                 p.style.border = "3px solid gold";
//                 p.style.backgroundColor = "rgba(255,255,0,0.1)";
//             }
//             else if (val === 3) {
//                 p.style.border = "3px solid red";
//                 p.style.backgroundColor = "rgba(255,0,0,0.1)";
//             }
//         });
//     }
// });


function startProcessing() {
    let elements = Array.from(document.querySelectorAll("p"));
    let list = elements.map(p => p.innerText);

    chrome.runtime.sendMessage({
        type: "P_LIST",
        list: list
    });

    // listen for results
    chrome.runtime.onMessage.addListener((msg) => {
        if (msg.type === "VALIDATION_RESULTS") {
            let results = msg.results;

            results.forEach((val, i) => {
                let p = elements[i];
                if (!p) return;

                if (val === 1) {
                    p.style.border = "3px solid limegreen";
                    p.style.backgroundColor = "rgba(0,255,0,0.1)";
                } else if (val === 2) {
                    p.style.border = "3px solid gold";
                    p.style.backgroundColor = "rgba(255,255,0,0.1)";
                } else if (val === 3) {
                    p.style.border = "3px solid red";
                    p.style.backgroundColor = "rgba(255,0,0,0.1)";
                }
            });
        }
    });
}

if (document.readyState === "complete") {
    // Page is already fully loaded
    startProcessing();
} else {
    // Wait for the load event
    window.addEventListener("load", startProcessing);
}

