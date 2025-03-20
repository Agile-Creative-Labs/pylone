class WebSocketChat {
    constructor() {
        this.socket = null;
        this.messageContainer = document.getElementById('messageContainer');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.connectButton = document.getElementById('connectButton');
        this.disconnectButton = document.getElementById('disconnectButton');
        this.statusDisplay = document.getElementById('status');

        this.initializeEventListeners();
    }

    updateStatus(connected) {
        if (connected) {
            this.statusDisplay.textContent = 'Connected';
            this.statusDisplay.className = 'connection-status connected';
        } else {
            this.statusDisplay.textContent = 'Disconnected';
            this.statusDisplay.className = 'connection-status disconnected';
        }
    }

    addMessage(text, isSent) {
        const messageElement = document.createElement('div');
        messageElement.textContent = text;
        messageElement.className = `message ${isSent ? 'sent' : 'received'}`;
        this.messageContainer.appendChild(messageElement);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }

    connect() {
        // Connect to the WebSocket server
        this.socket = new WebSocket('ws://127.0.0.1:8001/chat');

        this.socket.onopen = () => {
            this.updateStatus(true);
            this.addMessage('Connected to WebSocket server', false);
        };

        this.socket.onmessage = (event) => {
            this.addMessage(`Received: ${event.data}`, false);
        };

        this.socket.onclose = () => {
            this.updateStatus(false);
            this.addMessage('Disconnected from WebSocket server', false);
        };

        this.socket.onerror = (error) => {
            this.addMessage(`Error: ${error}`, false);
            this.updateStatus(false);
        };
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        if (message && this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(message);
            this.addMessage(`Sent: ${message}`, true);
            this.messageInput.value = '';
        }
    }

    initializeEventListeners() {
        this.connectButton.addEventListener('click', () => this.connect());
        this.disconnectButton.addEventListener('click', () => this.disconnect());
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
}

// Instantiate the WebSocketChat class
document.addEventListener('DOMContentLoaded', () => {
    const chatApp = new WebSocketChat();
});

