const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

sendBtn.addEventListener('click', () => {
    const msg = userInput.value.trim();
    if(msg === '') return;

    appendMessage(msg, 'user-msg');
    userInput.value = '';

    // Call backend API
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: msg})
    })
    .then(res => res.json())
    .then(data => appendMessage(data.reply, 'bot-msg'))
    .catch(err => appendMessage('Error: Could not reach server', 'bot-msg'));
});

function appendMessage(msg, className){
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', className);
    msgDiv.textContent = msg;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
