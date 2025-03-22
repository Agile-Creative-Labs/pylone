/**
 * WebSocketChat - A versatile WebSocket chat implementation with hybrid connection strategy
 * 
 * This class provides a complete implementation for chat functionality over WebSockets,
 * using a hybrid connection approach that balances performance and user experience.
 * It establishes connections on-demand when needed, maintains them during active use,
 * and closes them after periods of inactivity.
 * 
 * Features:
 * - Automatic connection when user focuses on input or sends a message
 * - Connection state management with visual feedback
 * - Automatic reconnection with exponential backoff
 * - Inactivity detection and automatic disconnection
 * - Promise-based connection API for better flow control
 * - Comprehensive error handling and recovery
 * - Optional debug logging
 * 
 * Usage:
 * const chat = new WebSocketChat({
 *     url: 'ws://your-server.com/chat',
 *     reconnectAttempts: 5,
 *     reconnectDelay: 3000,
 *     inactivityTimeout: 300000,  // 5 minutes
 *     autoReconnect: true,
 *     debug: false
 * });
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
 */
 // Enhanced WebSocketChat class

 class WebSocketChat 
 {
     constructor(options = {}) 
     {
         // Configuration options with defaults
         this.config = {
             url: options.url || 'ws://127.0.0.1:8001/chat',
             reconnectAttempts: options.reconnectAttempts || 5,
             reconnectDelay: options.reconnectDelay || 3000,
             inactivityTimeout: options.inactivityTimeout || 30000, // Default 30 seconds for testing
             autoReconnect: options.autoReconnect !== undefined ? options.autoReconnect : true,
             debug: options.debug !== undefined ? options.debug : false
         };

         // Connection state
         this.socket = null;
         this.isConnecting = false;
         this.reconnectCount = 0;
         this.inactivityTimer = null;

         // Cache DOM elements
         this.messageContainer = document.getElementById('messages');
         this.messageInput = document.getElementById('chat-input');
         this.sendButton = document.getElementById('sendButton');
         this.connectButton = document.getElementById('connectButton');
         this.disconnectButton = document.getElementById('disconnectButton');
         this.statusDisplay = document.getElementById('status');
         this.debugLogs = document.getElementById('debugLogs');

         // Validate required DOM elements
         this.validateElements();

         // Initialize event listeners
         this.initializeEventListeners();

         this.logDebug('WebSocketChat initialized');
     }

     /**
      * Validates that all required DOM elements exist.
      * Throws an error if any element is missing.
      */
     validateElements() 
     {
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
      * @param {string} status - Connection status ('connected', 'connecting', 'disconnected', 'error')
      */
     updateStatus(status) 
     {
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
         this.logDebug(`Status updated: ${status}`);
     }

     /**
      * Log debug information
      * @param {string} message - Debug message
      */
     logDebug(message) 
     {
         if (this.config.debug) {
             console.log(`[WebSocketChat] ${message}`);

             if (this.debugLogs) {
                 const logEntry = document.createElement('div');
                 logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
                 this.debugLogs.appendChild(logEntry);
                 this.debugLogs.scrollTop = this.debugLogs.scrollHeight;
             }
         }
     }

     /**
      * Adds a message to the message container.
      * @param {string} text - The message text.
      * @param {boolean} isSent - Whether the message was sent by the user.
      */
     addMessage(text, isSent) 
     {
         const messageElement = document.createElement('div');
         messageElement.textContent = text;
         messageElement.className = `message ${isSent ? 'sent' : 'received'}`;
         this.messageContainer.appendChild(messageElement);
         this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
         this.logDebug(`Message added: ${isSent ? 'Sent' : 'Received'} - ${text}`);
     }

     /**
      * Connects to the WebSocket server.
      * @returns {Promise} A promise that resolves when the connection is established
      */
     connect() 
     {
         // If already connected or connecting, just return the promise
         if (this.socket && this.socket.readyState === WebSocket.OPEN) {
             this.logDebug('Already connected');
             return Promise.resolve(this.socket);
         }

         if (this.isConnecting) {
             this.logDebug('Connection already in progress');
             return new Promise((resolve) => {
                 const checkInterval = setInterval(() => {
                     if (this.socket && this.socket.readyState === WebSocket.OPEN) {
                         clearInterval(checkInterval);
                         resolve(this.socket);
                     }
                 }, 100);
             });
         }

         // Reset inactivity timer if it exists
         this.resetInactivityTimer();

         // Start new connection
         this.isConnecting = true;
         this.updateStatus('connecting');
         this.logDebug(`Attempting to connect to ${this.config.url}`);

         return new Promise((resolve, reject) => {
             try {
                 this.socket = new WebSocket(this.config.url);

                 this.socket.onopen = () => {
                     this.isConnecting = false;
                     this.reconnectCount = 0;
                     this.updateStatus('connected');
                     this.addMessage('Connected to WebSocket server', false);
                     this.resetInactivityTimer();
                     this.logDebug('Connection established');
                     resolve(this.socket);
                 };

                 this.socket.onmessage = (event) => {
                     this.resetInactivityTimer(); // Reset timer on activity
                     this.addMessage(`Received: ${event.data}`, false);
                     this.logDebug(`Message received: ${event.data}`);
                 };

                 this.socket.onclose = (event) => {
                     this.isConnecting = false;
                     this.updateStatus('disconnected');
                     this.addMessage('Disconnected from WebSocket server', false);
                     this.logDebug(`Connection closed: ${event.wasClean ? 'Clean' : 'Unclean'} - Code: ${event.code}`);

                     // Attempt to reconnect if not a deliberate close
                     if (this.config.autoReconnect && !event.wasClean) {
                         this.attemptReconnect();
                     }

                     if (event.wasClean) {
                         resolve(null); // Deliberate closure
                     } else {
                         reject(new Error('Connection closed unexpectedly'));
                     }
                 };

                 this.socket.onerror = (error) => {
                     this.isConnecting = false;
                     this.updateStatus('error');
                     this.addMessage(`Error: ${error.message || 'WebSocket error'}`, false);
                     this.logDebug(`Connection error: ${error.message || 'Unknown error'}`);
                     reject(error);
                 };
             } catch (error) {
                 this.isConnecting = false;
                 this.updateStatus('error');
                 this.addMessage(`Connection error: ${error.message}`, false);
                 this.logDebug(`Connection error: ${error.message}`);
                 reject(error);
             }
         });
     }

     /**
      * Force a reconnection attempt by closing and reopening
      */
     forceReconnect() 
     {
         this.logDebug('Force reconnect initiated');

         if (this.socket) {
             const wasConnected = this.socket.readyState === WebSocket.OPEN;
             this.socket.close();

             if (wasConnected) {
                 this.connect().catch(error => {
                     this.logDebug(`Force reconnect error: ${error.message}`);
                 });
             }
         } else {
             this.connect().catch(error => {
                 this.logDebug(`Force reconnect error: ${error.message}`);
             });
         }
     }

     /**
      * Simulate an error for testing
      */
     simulateError() 
     {
         this.logDebug('Simulating connection error');
         if (this.socket && this.socket.readyState === WebSocket.OPEN) {
             // Force close with an error code
             this.socket.close(4000, "Simulated error");
         } else {
             this.addMessage('Cannot simulate error: No active connection', false);
         }
     }

     /**
      * Attempts to reconnect to the WebSocket server after a delay.
      * Uses exponential backoff for retry intervals.
      */
     attemptReconnect() 
     {
         if (this.reconnectCount >= this.config.reconnectAttempts) {
             this.addMessage('Maximum reconnection attempts reached', false);
             this.logDebug('Maximum reconnection attempts reached');
             return;
         }

         this.reconnectCount++;
         const delay = this.reconnectCount * this.config.reconnectDelay;

         this.addMessage(`Attempting to reconnect in ${delay/1000} seconds...`, false);
         this.updateStatus('connecting');
         this.logDebug(`Scheduling reconnect attempt ${this.reconnectCount} in ${delay/1000} seconds`);

         setTimeout(() => {
             this.logDebug(`Executing reconnect attempt ${this.reconnectCount}`);
             this.connect().catch((error) => {
                 this.logDebug(`Reconnect attempt ${this.reconnectCount} failed: ${error.message}`);
             });
         }, delay);
     }

     /**
      * Disconnects from the WebSocket server.
      */
     disconnect() 
     {
         clearTimeout(this.inactivityTimer);
         this.inactivityTimer = null;

         if (this.socket) {
             this.logDebug('Disconnecting...');
             this.socket.close(1000, "Deliberate disconnection");
             this.socket = null;
             this.updateStatus('disconnected');
         }
     }

     /**
      * Reset the inactivity timer that will close the connection after a period of inactivity
      */
     resetInactivityTimer() 
     {
         clearTimeout(this.inactivityTimer);

         if (this.config.inactivityTimeout > 0) {
             this.logDebug(`Resetting inactivity timer (${this.config.inactivityTimeout}ms)`);
             this.inactivityTimer = setTimeout(() => {
                 this.addMessage('Disconnected due to inactivity', false);
                 this.updateStatus('inactive');
                 this.logDebug('Inactivity timeout reached');
                 this.disconnect();
             }, this.config.inactivityTimeout);
         }
     }

     /**
      * Set a new inactivity timeout value
      * @param {number} timeout - New timeout in milliseconds
      */
     setInactivityTimeout(timeout) 
     {
         if (timeout >= 0) {
             this.config.inactivityTimeout = timeout;
             this.logDebug(`Inactivity timeout updated to ${timeout}ms`);
             this.resetInactivityTimer();
         }
     }

     /**
      * Clear all messages from the display
      */
     clearMessages() 
     {
         while (this.messageContainer.firstChild) {
             this.messageContainer.removeChild(this.messageContainer.firstChild);
         }
         this.logDebug('Messages cleared');
     }

     /**
      * Toggle debug logging
      */
     toggleDebugLogging() 
     {
         this.config.debug = !this.config.debug;
         this.logDebug(`Debug logging ${this.config.debug ? 'enabled' : 'disabled'}`);
         return this.config.debug;
     }

     /**
      * Sends a message through the WebSocket connection.
      * Handles automatic reconnection if needed.
      */
     sendMessage() 
     {
         const message = this.messageInput.value.trim();
         if (!message) {
             this.logDebug('Empty message, not sending');
             return;
         }

         // If socket is closed or doesn't exist, try to connect first
         if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
             this.logDebug('Not connected, connecting before sending');
             this.connect()
                 .then(() => this._sendMessageToSocket(message))
                 .catch(error => {
                     this.addMessage(`Failed to connect: ${error.message}`, false);
                     this.logDebug(`Connection failure when trying to send: ${error.message}`);
                 });
             return;
         }

         this._sendMessageToSocket(message);
     }

     /**
      * Internal method to send a message once the socket is connected
      * @param {string} message - The message to send
      */
     _sendMessageToSocket(message) 
     {
         try {
             this.socket.send(message);
             this.addMessage(`Sent: ${message}`, true);
             this.messageInput.value = '';
             this.resetInactivityTimer();
             this.logDebug(`Message sent: ${message}`);
         } catch (error) {
             this.addMessage(`Failed to send message: ${error.message}`, false);
             this.logDebug(`Send error: ${error.message}`);
         }
     }

     /**
      * Initializes event listeners for UI interactions.
      */
     initializeEventListeners() 
     {
         this.connectButton.addEventListener('click', () => this.connect());
         this.disconnectButton.addEventListener('click', () => this.disconnect());
         this.sendButton.addEventListener('click', () => this.sendMessage());

         this.messageInput.addEventListener('keypress', (e) => {
             if (e.key === 'Enter') {
                 this.sendMessage();
             }
         });

         // Connect automatically when the user interacts with the input
         this.messageInput.addEventListener('focus', () => {
             if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
                 this.connect().catch(error => {
                     this.logDebug(`Connection error on focus: ${error.message}`);
                 });
             }
         });

         // Reset inactivity timer on user interactions
         const resetTimerEvents = ['input', 'click', 'focus'];
         resetTimerEvents.forEach(event => {
             this.messageInput.addEventListener(event, () => this.resetInactivityTimer());
         });
     }
 }

 // Initialize the chat with debug mode enabled for testing
 /*
 document.addEventListener('DOMContentLoaded', () => {
     const chat = new WebSocketChat({
         url: 'ws://localhost:8001/chat',
         reconnectAttempts: 5,
         reconnectDelay: 3000,
         inactivityTimeout: 30000, // 30 seconds for testing
         autoReconnect: true,
         debug: true
     });

     // Setup debug controls
     document.getElementById('toggleLogging').addEventListener('click', () => {
         const isEnabled = chat.toggleDebugLogging();
         document.getElementById('toggleLogging').textContent =
             isEnabled ? 'Disable Console Logging' : 'Enable Console Logging';
     });

     document.getElementById('forceReconnect').addEventListener('click', () => {
         chat.forceReconnect();
     });

     document.getElementById('simulateError').addEventListener('click', () => {
         chat.simulateError();
     });

     document.getElementById('clearMessages').addEventListener('click', () => {
         chat.clearMessages();
     });

     document.getElementById('updateTimeout').addEventListener('click', () => {
         const timeoutValue = parseInt(document.getElementById('inactivityTimeout').value);
         if (!isNaN(timeoutValue) && timeoutValue >= 5000) {
             chat.setInactivityTimeout(timeoutValue);
         }
     });
 });*/