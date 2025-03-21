class WebSocketChat {
    constructor() {
        // Cache DOM elements
        this.messageContainer = document.getElementById('messageContainer');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.connectButton = document.getElementById('connectButton');
        this.disconnectButton = document.getElementById('disconnectButton');
        this.statusDisplay = document.getElementById('status');

        // Validate required DOM elements
        this.validateElements();

        // Initialize WebSocket and event listeners
        this.socket = null;
        this.initializeEventListeners();
    }

    /**
     * Validates that all required DOM elements exist.
     * Throws an error if any element is missing.
     */
    validateElements() {
        const elements = {
            messageContainer: this.messageContainer,
            messageInput: this.messageInput,
            sendButton: this.sendButton,
            connectButton: this.connectButton,
            disconnectButton: this.disconnectButton,
            statusDisplay: this.statusDisplay,
        };

        for (const [name, element] of Object.entries(elements)) {
            if (!element) {
                throw new Error(`Required element "${name}" is missing.`);
            }
        }
    }

    /**
     * Updates the connection status display.
     * @param {boolean} connected - Whether the connection is active.
     */
    updateStatus(connected) {
        this.statusDisplay.textContent = connected ? 'Connected' : 'Disconnected';
        this.statusDisplay.className = `connection-status ${connected ? 'connected' : 'disconnected'}`;
    }

    /**
     * Adds a message to the message container.
     * @param {string} text - The message text.
     * @param {boolean} isSent - Whether the message was sent by the user.
     */
    addMessage(text, isSent) {
        const messageElement = document.createElement('div');
        messageElement.textContent = text;
        messageElement.className = `message ${isSent ? 'sent' : 'received'}`;
        this.messageContainer.appendChild(messageElement);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }

    /**
     * Connects to the WebSocket server.
     */
    connect() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.warn('WebSocket is already connected.');
            return;
        }

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
            this.addMessage(`Error: ${error.message || 'WebSocket error'}`, false);
            this.updateStatus(false);
        };
    }

    /**
     * Disconnects from the WebSocket server.
     */
    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }

    /**
     * Sends a message through the WebSocket connection.
     */
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) {
            console.warn('Message cannot be empty.');
            return;
        }

        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            console.warn('WebSocket is not connected.');
            return;
        }

        try {
            this.socket.send(message);
            this.addMessage(`Sent: ${message}`, true);
            this.messageInput.value = '';
        } catch (error) {
            this.addMessage(`Failed to send message: ${error.message}`, false);
        }
    }

    /**
     * Initializes event listeners for UI interactions.
     */
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
