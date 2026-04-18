const chatId = JSON.parse(document.getElementById('chat-id').textContent);
const loggedInUser = JSON.parse(document.getElementById('user-username').textContent);
const container = document.getElementById('message-container');
const messageInput = document.querySelector('#chat-message-input');
const sendButton = document.querySelector('#chat-message-submit');
const typingIndicator = document.getElementById('typing-indicator');

const chatSocket = new WebSocket((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/chat/' + chatId + '/');

// 1. Tell the server we have opened the chat (trigger read receipt)
chatSocket.onopen = () => {
    chatSocket.send(JSON.stringify({'type': 'read_receipt'}));
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    // Update checkmarks to ✓✓ if the OTHER user reads messages
    if (data.type === 'messages_read' && data.reader !== loggedInUser) {
        document.querySelectorAll('.status-icon').forEach(icon => {
            icon.innerHTML = '✓✓';
        });
    } 
    // Handle Typing status
    else if (data.type === 'typing' && data.sender !== loggedInUser) {
        typingIndicator.innerText = data.is_typing ? `${data.sender} is typing...` : '';
    } 
    // Display new message
    else if (data.type === 'chat_message') {
        const isMe = data.sender === loggedInUser;
        const msgHtml = `
            <div class="flex ${isMe ? 'justify-end' : 'justify-start'}">
                <div class="max-w-[75%] rounded-2xl px-4 py-2 shadow-sm ${isMe ? 'bg-blue-500 text-white rounded-tr-none' : 'bg-white text-gray-800 border rounded-tl-none'}">
                    <p class="font-bold font-sans">${data.message}</p>
                    <span class="text-[10px] opacity-70 block text-right">
                        Just now ${isMe ? '<span class="status-icon">✓</span>' : ''}
                    </span>
                </div>
            </div>`;
        container.insertAdjacentHTML('beforeend', msgHtml);
        container.scrollTop = container.scrollHeight;
        
        // If I receive a message while I'm looking at it, send a read receipt back
        if (!isMe) {
            chatSocket.send(JSON.stringify({'type': 'read_receipt'}));
        }
    }
};

// 2. Typing/Sending Logic
let typingTimeout;
messageInput.oninput = () => {
    chatSocket.send(JSON.stringify({'type': 'typing', 'typing': true}));
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        chatSocket.send(JSON.stringify({'type': 'typing', 'typing': false}));
    }, 2000);
};

const handleSend = () => {
    if (messageInput.value.trim()) {
        chatSocket.send(JSON.stringify({'type': 'chat_message', 'message': messageInput.value}));
        messageInput.value = '';
        chatSocket.send(JSON.stringify({'type': 'typing', 'typing': false}));
    }
};

sendButton.onclick = handleSend;
messageInput.onkeyup = (e) => { if (e.keyCode === 13 && !e.shiftKey) { e.preventDefault(); handleSend(); } };
