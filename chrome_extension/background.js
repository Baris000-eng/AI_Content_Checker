// let socket = new WebSocket("ws://127.0.0.1:8765");

// socket.onopen = () => console.log("WS CONNECTED");
// socket.onerror = (e) => console.log("WS ERROR", e);
// socket.onclose = () => console.log("WS CLOSED");

// let currentTabId = null;

// chrome.runtime.onMessage.addListener((msg, sender) => {
//     if (msg.type === "P_LIST") {

//         currentTabId = sender.tab.id;

//         let paragraphs = msg.list;
//         let index = 0;

//         function sendNext() {
//             if (index >= paragraphs.length) return;

//             if (socket.readyState === WebSocket.OPEN) {
//                 socket.send(paragraphs[index]);
//                 index++;
//                 setTimeout(sendNext, 10);
//             } else {
//                 setTimeout(sendNext, 100);
//             }
//         }

//         sendNext();
//     }
// });

// // Receive validation from Python and forward to the webpage
// socket.onmessage = (event) => {
//     let data = JSON.parse(event.data);

//     chrome.tabs.sendMessage(currentTabId, {
//         type: "VALIDATION_RESULT",
//         index: data.index,
//         result: data.result
//     });
// };

let socket = new WebSocket("ws://127.0.0.1:8765");

socket.onopen = () => console.log("WS CONNECTED");
socket.onerror = (e) => console.log("WS ERROR", e);
socket.onclose = () => console.log("WS CLOSED");

let currentTabId = null;

// Receive list from content.js
chrome.runtime.onMessage.addListener((msg, sender) => {
    if (msg.type === "P_LIST") {

        currentTabId = sender.tab.id;

        // Send the entire array at once
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(msg.list));
        } else {
            console.log("Socket not open");
        }
    }
});

// Receive results array from Python
socket.onmessage = (event) => {
    let data = JSON.parse(event.data);

    chrome.tabs.sendMessage(currentTabId, {
        type: "VALIDATION_RESULTS",
        results: data.results
    });
};
