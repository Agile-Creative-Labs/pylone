class ChatApp {
    constructor() {
        // Cache DOM elements
        this.chatInput = document.getElementById('chatInput');
        this.chatHistory = document.getElementById('chatHistory');
        this.welcomeContainer = document.getElementById('welcomeContainer');
        this.actionCardsContainer = document.getElementById('actionCardsContainer');
        this.sendBtn = document.getElementById('sendBtn');

        // Validate required DOM elements
        this.validateElements();

        // Initialize event listeners
        this.initializeEventListeners();
    }

    /**
     * Validates that all required DOM elements exist.
     * Throws an error if any element is missing.
     */
    validateElements() {
        const elements = {
            chatInput: this.chatInput,
            chatHistory: this.chatHistory,
            welcomeContainer: this.welcomeContainer,
            actionCardsContainer: this.actionCardsContainer,
            sendBtn: this.sendBtn,
        };

        for (const [name, element] of Object.entries(elements)) {
            if (!element) {
                throw new Error(`Required element "${name}" is missing.`);
            }
        }
    }

    /**
     * Initializes event listeners.
     */
    initializeEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    /**
     * Sends a message.
     * @param {string} predefinedMessage - An optional predefined message to send.
     */
    sendMessage(predefinedMessage = '') {
        const userMessage = predefinedMessage || this.chatInput.value.trim();

        if (userMessage) {
            // Hide welcome and action cards sections
            this.welcomeContainer.classList.add('hidden');
            this.actionCardsContainer.classList.add('hidden');

            // Append user message to chat history
            this.appendMessage(userMessage, true);

            // Clear input if not a predefined message
            if (!predefinedMessage) {
                this.chatInput.value = '';
            }

            // Simulate bot response after 1 second
            this.simulateBotResponse();
        }
    }

    /**
     * Appends a message to the chat history.
     * @param {string} text - The message text.
     * @param {boolean} isSent - Whether the message was sent by the user.
     */
    __appendMessage(text, isSent) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('d-flex', 'align-items-start', 'mb-3', 'fade-up');

        const profileImage = document.createElement('img');
        profileImage.src = isSent ? '/static/images/pfpuser.png' : '/static/images/pfpbot.png';
        profileImage.alt = isSent ? 'User' : 'Bot';
        profileImage.classList.add('rounded-circle', 'me-2');
        profileImage.style.width = '40px';
        profileImage.style.marginTop = '0.5rem';

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('alert', 'text-start', 'flex-grow-1');
        messageDiv.style.backgroundColor = isSent ? '#d1e7dd' : '#ffffff'; // Different colors for sent/received
        messageDiv.style.border = '1px solid #dee2e6';
        messageDiv.style.borderRadius = '0.25rem';
        messageDiv.innerHTML = `<strong>${isSent ? 'You:' : 'Fluwd:'}</strong> ${text}`;

        messageContainer.appendChild(profileImage);
        messageContainer.appendChild(messageDiv);
        this.chatHistory.appendChild(messageContainer);

        // Scroll to the bottom of the chat history
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }
     //
    /**
 * Appends a message to the chat history.
 * @param {string} text - The message text.
 * @param {boolean} isSent - Whether the message was sent by the user.
 */

appendMessage(text, isSent) {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('d-flex', 'align-items-start', 'mb-3', 'fade-up');

    const profileImage = document.createElement('img');
    profileImage.src = isSent ? '/static/images/pfpuser.png' : '/static/images/pfpbot.png';
    profileImage.alt = isSent ? 'User' : 'Bot';
    profileImage.classList.add('rounded-circle', 'me-2');
    profileImage.style.width = '40px';
    profileImage.style.marginTop = '0.5rem';

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('alert', 'text-start', 'flex-grow-1');
    messageDiv.style.backgroundColor = isSent ? '#d1e7dd' : '#ffffff'; // Different colors for sent/received
    messageDiv.style.border = '1px solid #dee2e6';
    messageDiv.style.borderRadius = '0.25rem';
    messageDiv.innerHTML = `<strong>${isSent ? 'You:' : 'Fluwd:'}</strong> ${text}`;

    messageContainer.appendChild(profileImage);
    messageContainer.appendChild(messageDiv);
    this.chatHistory.appendChild(messageContainer);

    // Scroll to the bottom of the chat history
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
}


    /**
     * Simulates a bot response.
     */
    simulateBotResponse() {
        // Show loading indicator
        const loadingIndicator = this.createLoadingIndicator();
        this.chatHistory.appendChild(loadingIndicator);

        // Simulate a delay for the bot response
        setTimeout(() => {
            // Remove loading indicator
            this.chatHistory.removeChild(loadingIndicator);

            // Append bot response
            const botResponse = this.generateBotResponse();
            this.appendMessage(botResponse, false);

            // Append regenerate button
            this.appendRegenerateButton();
        }, 1000); // 1-second delay
    }

    /**
     * Creates a loading indicator.
     * @returns {HTMLElement} - The loading indicator element.
     */
    createLoadingIndicator() {
        const loadingContainer = document.createElement('div');
        loadingContainer.classList.add('d-flex', 'align-items-start', 'mb-3', 'fade-up');

        const botImage = document.createElement('img');
        botImage.src = '/static/images/pfpbot.png';
        botImage.alt = 'Fluwd';
        botImage.classList.add('rounded-circle', 'me-2');
        botImage.style.width = '40px';
        botImage.style.marginTop = '0.5rem';

        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('alert', 'text-start', 'flex-grow-1');
        loadingDiv.style.backgroundColor = '#ffffff';
        loadingDiv.style.border = '1px solid #dee2e6';
        loadingDiv.style.borderRadius = '0.25rem';
        loadingDiv.innerHTML = `<strong>Fluwd:</strong> Thinking...`;

        loadingContainer.appendChild(botImage);
        loadingContainer.appendChild(loadingDiv);

        return loadingContainer;
    }

    /**
     * Generates a simulated bot response.
     * @returns {string} - The bot response.
     */
    generateBotResponse() {
        return `
            To resolve issues of a delayed project schedule, consider implementing the following strategies:
            <ol>
                <li><strong>Conduct a Root Cause Analysis:</strong> Identify the reasons behind the delays.</li>
                <li><strong>Re-Evaluate and Adjust the Project Plan:</strong> Break down tasks and prioritize critical activities.</li>
                <li><strong>Improve Communication:</strong> Hold frequent status meetings and ensure clear communication channels.</li>
            </ol>
        `;
    }

    /**
     * Appends a "Regenerate Response" button to the chat history.
     */
    appendRegenerateButton() {
        const regenerateContainer = document.createElement('div');
        regenerateContainer.classList.add('text-center', 'mt-3', 'mb-4');
        regenerateContainer.style.marginLeft = '15px';
        regenerateContainer.style.marginRight = '15px';

        const regenerateButton = document.createElement('button');
        regenerateButton.classList.add('btn', 'mt-3');
        regenerateButton.style.backgroundColor = '#ffffff';
        regenerateButton.style.color = '#6c757d';
        regenerateButton.style.border = 'none';
        regenerateButton.style.padding = '10px 20px';
        regenerateButton.style.borderRadius = '20px';
        regenerateButton.style.boxShadow = '0px 2px 5px rgba(0, 0, 0, 0.1)';
        regenerateButton.innerHTML = `<i class="bi bi-arrow-clockwise me-2"></i> Regenerate response`;

        // Add click event to regenerate the response
        regenerateButton.onclick = () => {
            this.sendMessage("What should I do to help resolve the issue of delayed project schedule?");
        };

        regenerateContainer.appendChild(regenerateButton);
        this.chatHistory.appendChild(regenerateContainer);
    }
}


