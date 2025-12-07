const API_URL = "http://127.0.0.1:8000/ask";

async function sendMessage() {
    const userInput = document.getElementById("userInput").value.trim();
    const language = document.getElementById("language").value;
    const chatBox = document.getElementById("chatBox");

    if (!userInput) return;

    // Add user message to chat
    chatBox.innerHTML += `<div class='user-msg'>${userInput}</div>`;

    // Clear input
    document.getElementById("userInput").value = "";

    // Send request to backend
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_query: userInput, language })
        });

        const data = await response.json();

        if (data.reply) {
            chatBox.innerHTML += `<div class='bot-msg'>${data.reply}</div>`;
        } else {
            chatBox.innerHTML += `<div class='bot-msg error'>Error: ${data.error}</div>`;
        }

    } catch (e) {
        chatBox.innerHTML += `<div class='bot-msg error'>Network error!</div>`;
    }

    // Auto-scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Allow Enter key to send
function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}