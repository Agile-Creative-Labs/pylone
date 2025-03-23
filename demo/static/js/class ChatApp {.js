/**
 * FluwdChatApp - A versatile WebSocket chat implementation with hybrid connection strategy
 * 
 * This class provides a complete implementation for chat functionality over WebSockets,
 * using a hybrid connection approach that balances performance and user experience.
 * It establishes connections on-demand when needed, maintains them during active use,
 * and closes them after periods of inactivity.
 * 
 * Features:
 * - WebSocket connection with auto-reconnect and inactivity timeout handling.
 * - Transition effects from the welcome screen to chat view.
 * - Bot typing indicator and dynamic responses.
 * - Secure message handling with HTML sanitization.
 * - Configurable via initialization parameters.
 * 
 * 
 *
 * @param {Object} options - Configuration object.
 * @param {string} options.url - WebSocket server URL.
 * @param {number} options.reconnectAttempts - Maximum reconnection attempts.
 * @param {number} options.reconnectDelay - Delay between reconnection attempts (ms).
 * @param {number} options.inactivityTimeout - Time before inactivity triggers disconnect (ms).
 * @param {boolean} options.autoReconnect - Whether to automatically reconnect on disconnect.
 * @param {boolean} options.debug - Enable debug logging.
 * 
 * DOM Requirements:
 * - #messages: Container for displaying chat messages
 * - #messageInput: Text input for new messages
 * - #sendButton: Button to send messages
 * - #connectButton: Button to manually connect
 * - #disconnectButton: Button to manually disconnect
 * - #status: Element for displaying connection status
 * 
 * @author Agile Creative Labs Inc
 * @version 1.0.0
 * @license MIT
 * @date 22 Mar 2025
 * 
 * 
 *  * Usage:
 * const chat = new FluwdChatApp({
 *     url: 'ws://your-server.com/chat',
 *     reconnectAttempts: 5,
 *     reconnectDelay: 3000,
 *     inactivityTimeout: 300000,  // 5 minutes
 *     autoReconnect: true,
 *     debug: false
 * });
 * 
 *  */

class FluwdChatApp {
    constructor(options = {}) {
        // Default settings
        this.settings = Object.assign({
            url: '',
            reconnectAttempts: 5,
            reconnectDelay: 3000,
            maxReconnectDelay: 30000, // Maximum delay between reconnection attempts
            inactivityTimeout: 30000, // Default inactivity timeout
            typingGracePeriod: 180000, // 3-minute grace period after typing stops
            autoReconnect: true,
            debug: true, // Enable debug mode
        }, options);

        // DOM elements
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');
        this.messages = document.getElementById('messages');
        this.welcomeCard = document.querySelector('.welcome-card');
        this.featureContainer = document.querySelector('.feature-container');
        this.chatContainer = document.querySelector('.chat-container');
        this.statusDisplay = document.getElementById('status');

        // WebSocket properties
        this.socket = null;
        this.reconnectAttempts = 0;
        this.inactivityTimer = null;
        this.typingTimer = null; // Timer for typing grace period

        // Bind methods
        this.handleSubmit = this.handleSubmit.bind(this);
        this.scrollToBottom = this.scrollToBottom.bind(this);
        this.handleKeypress = this.handleKeypress.bind(this);
        this.addBotMessage = this.addBotMessage.bind(this); // Ensure this method is bound

        // Initialize
        this.initEventListeners();
        this.initWebSocket(); // Explicitly call initWebSocket to establish the connection
        setTimeout(this.scrollToBottom, 100);
    }

    initEventListeners() {
        this.chatForm.addEventListener('submit', this.handleSubmit);
        this.chatInput.addEventListener('keypress', this.handleKeypress); // Listen for keypress
        window.addEventListener('load', () => setTimeout(this.scrollToBottom, 200));
    }

    handleKeypress() {
        // Reset the inactivity timer on every keypress
        this.resetInactivityTimer();

        // Clear the typing grace period timer
        clearTimeout(this.typingTimer);

        // Start a new grace period timer after typing stops
        this.typingTimer = setTimeout(() => {
            this.log('User stopped typing. Starting inactivity timer.');
            this.resetInactivityTimer(); // Restart the inactivity timer
        }, this.settings.typingGracePeriod); // 3-minute grace period
    }

    initWebSocket() {
        if (!this.settings.url) {
            this.log('WebSocket URL is not provided.');
            return;
        }

        this.log('Connecting to WebSocket...');
        this.log('WebSocket URL:', this.settings.url); // Log the WebSocket URL
        this.updateStatus('connecting');

        try {
            this.socket = new WebSocket(this.settings.url);

            this.socket.onopen = () => {
                this.log('WebSocket connected.');
                this.updateStatus('connected');
                this.reconnectAttempts = 0;
                this.resetInactivityTimer();
            };

            this.socket.onmessage = (event) => {
                this.log('WebSocket message received:', event.data);
                this.resetInactivityTimer();
                this.addBotMessage(event.data);
            };

            this.socket.onclose = (event) => {
                this.log('WebSocket disconnected. Code:', event.code, 'Reason:', event.reason);
                this.updateStatus('disconnected');

                if (this.settings.autoReconnect && this.reconnectAttempts < this.settings.reconnectAttempts) {
                    const delay = Math.min(this.settings.reconnectDelay * Math.pow(2, this.reconnectAttempts), this.settings.maxReconnectDelay);
                    this.reconnectAttempts++;
                    this.log(`Attempting to reconnect in ${delay}ms...`);
                    setTimeout(() => this.initWebSocket(), delay);
                }
            };

            this.socket.onerror = (error) => {
                this.log('WebSocket error:', error);
                this.updateStatus('error');
            };
        } catch (error) {
            this.log('WebSocket initialization error:', error);
            this.updateStatus('error');
        }
    }

    handleSubmit(e) {
        e.preventDefault();
        const message = this.chatInput.value.trim();
        if (!message) return;

        this.addUserMessage(message);
        this.transitionToChatView(() => {
            this.showBotTyping();
            this.sendMessage(message);
        });
        this.chatInput.value = '';
    }

    sendMessage(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.log('Sending message:', message);
            this.socket.send(message);
        } else {
            this.log('WebSocket not connected. Falling back to local processing.');
            this.processBotResponse(message);
        }
    }

    resetInactivityTimer() {
        clearTimeout(this.inactivityTimer);
        this.inactivityTimer = setTimeout(() => {
            this.log('User inactive. Disconnecting WebSocket.');
            this.socket?.close();
        }, this.settings.inactivityTimeout);
    }

    transitionToChatView(callback) {
        this.featureContainer.style.opacity = '0';
        this.welcomeCard.style.opacity = '0';
        setTimeout(() => {
            this.featureContainer.style.display = 'none';
            this.welcomeCard.style.display = 'none';
            this.chatContainer.style.display = 'block';
            setTimeout(() => {
                this.chatContainer.style.opacity = '1';
                if (callback) callback();
            }, 50);
        }, 500);
    }

    addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message-wrapper user-container';
        messageDiv.innerHTML = `<div class="user-message">${this.sanitizeHTML(message)}</div><div class="user-icon"><i class="fas fa-user"></i></div>`;
        this.messages.appendChild(messageDiv);
        setTimeout(this.scrollToBottom, 50);
    }

    addBotMessage(message) {
        this.hideBotTyping();
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message-wrapper bot-container';
        messageDiv.innerHTML = `<div class="bot-icon"><i class="fas fa-robot"></i></div><div class="bot-message">${this.sanitizeHTML(message)}</div>`;
        this.messages.appendChild(messageDiv);
        setTimeout(this.scrollToBottom, 50);
    }

    showBotTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message-wrapper bot-container';
        typingDiv.id = 'bot-typing';
        typingDiv.innerHTML = `<div class="bot-icon"><i class="fas fa-robot"></i></div><div class="bot-message bot-typing"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>`;
        this.messages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideBotTyping() {
        document.getElementById('bot-typing')?.remove();
    }

    scrollToBottom() {
        requestAnimationFrame(() => {
            this.messages.scrollTop = this.messages.scrollHeight;
        });
    }

    sanitizeHTML(text) {
        const element = document.createElement('div');
        element.textContent = text;
        return element.innerHTML;
    }

    log(...args) {
        if (this.settings.debug) console.log('[ChatApp]', ...args);
    }

    updateStatus(status) {
        const statusMap = {
            'connected': {
                text: 'Connected',
                className: 'connected'
            },
            'connecting': {
                text: 'Connecting...',
                className: 'connecting'
            },
            'disconnected': {
                text: 'Disconnected',
                className: 'disconnected'
            },
            'error': {
                text: 'Connection Error',
                className: 'error'
            },
            'inactive': {
                text: 'Inactive',
                className: 'inactive'
            }
        };

        const statusInfo = statusMap[status] || statusMap.disconnected;

        this.statusDisplay.textContent = statusInfo.text;
        this.statusDisplay.className = `connection-status ${statusInfo.className}`;
        console.log(`Status updated: ${status}`);
    }
}