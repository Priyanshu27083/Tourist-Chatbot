const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const typing = document.getElementById("typing");

function appendMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);

  // Convert simple Markdown (bold, bullets) to HTML
  const formatted = text
    .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")  // bold
    .replace(/\*(.*?)\*/g, "<i>$1</i>")      // italics
    .replace(/(?:\r\n|\r|\n)/g, "<br>")      // new lines

  msg.innerHTML = formatted; // ✅ render HTML
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}


async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  appendMessage(`You: ${text}`, "user");
  input.value = "";
  typing.style.display = "block";

  const response = await fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  });

  const data = await response.json();

  setTimeout(() => {
    typing.style.display = "none";
    appendMessage(`TourMate: ${data.reply}`, "bot");
  }, 1000 + Math.random() * 1000);
}
