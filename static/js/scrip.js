document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        // 添加用户消息到聊天窗口
        addMessage('user', message);
        userInput.value = '';

        // 发送消息到后端 API
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage('ai', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('ai', 'Sorry, something went wrong. Please try again later.');
        });
    }

    function addMessage(sender, text) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = text;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // 按回车键发送消息
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});