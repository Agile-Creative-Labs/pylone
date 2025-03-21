class ChatApp {
    constructor() {
        this.chatInput = document.getElementById('chatInput');
        this.chatHistory = document.getElementById('chatHistory');
        this.welcomeContainer = document.getElementById('welcomeContainer');
        this.actionCardsContainer = document.getElementById('actionCardsContainer');
        this.sendBtn = document.getElementById('sendBtn');

        // Check if elements exist before adding event listeners
        if (this.sendBtn) {
            this.initialize();
        } else {
            console.error('Send button not found!');
        }
    }

    initialize() {
        // Add event listener for the send button
        this.sendBtn.addEventListener('click', () => this.sendMessage());
    }

    sendMessage(predefinedMessage = '') {
        const userMessage = predefinedMessage || this.chatInput.value.trim();

        if (userMessage !== '') {
            // Hide elements
            this.welcomeContainer.classList.add('hidden');
            this.actionCardsContainer.classList.add('hidden');

            // Append user message to chat history
            this.appendUserMessage(userMessage);

            // Clear chat input if not a predefined message
            if (!predefinedMessage) {
                this.chatInput.value = '';
            }

            // Simulate chatbot response after 1 second
            setTimeout(() => {
                this.appendBotResponse();
                this.appendRegenerateButton();
            }, 1000);
        }
    }

    appendUserMessage(message) {
        const userMessageContainer = document.createElement('div');
        userMessageContainer.classList.add('d-flex', 'align-items-start', 'mb-3', 'fade-up');

        const userImage = document.createElement('img');
        userImage.src = '/static/images/pfpuser.png'; // User profile image
        userImage.alt = 'User';
        userImage.classList.add('rounded-circle', 'me-2');
        userImage.style.width = '40px';
        userImage.style.marginTop = '0.5rem';

        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('alert', 'alert-primary', 'text-start', 'flex-grow-1');
        userMessageDiv.innerHTML = `<strong>You:</strong> ${message}`;

        userMessageContainer.appendChild(userImage);
        userMessageContainer.appendChild(userMessageDiv);
        this.chatHistory.appendChild(userMessageContainer);

        // Scroll to the bottom of chat history
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }

    appendBotResponse() {
        const responseMessageContainer = document.createElement('div');
        responseMessageContainer.classList.add('d-flex', 'align-items-start', 'mb-3', 'fade-up');

        const botImage = document.createElement('img');
        botImage.src = '/static/images/pfpbot.png'; // Bot profile image
        botImage.alt = 'Fluwd';
        botImage.classList.add('rounded-circle', 'me-2');
        botImage.style.width = '40px';
        botImage.style.marginTop = '0.5rem';

        const responseMessageDiv = document.createElement('div');
        responseMessageDiv.classList.add('alert', 'text-start', 'flex-grow-1');
        responseMessageDiv.style.backgroundColor = '#ffffff';
        responseMessageDiv.style.color = '#000000';
        responseMessageDiv.style.border = '1px solid #dee2e6';
        responseMessageDiv.style.borderRadius = '0.25rem';
        responseMessageDiv.innerHTML = `
            <strong>Fluwd:</strong>
            <p>To resolve issues of a delayed project schedule, consider implementing the following strategies:</p>
            <p><strong>Strategies to Resolve Delayed Project Schedules</strong></p>
            <ol>
                <li>
                    <strong>Conduct a Root Cause Analysis</strong><br>
                    Identify the reasons behind the delays. Common causes can include scope creep, resource shortages, technical challenges, or inadequate planning.
                </li>
                <li>
                    <strong>Re-Evaluate and Adjust the Project Plan</strong><br>
                    <ul>
                        <li>Break Down Tasks: Ensure tasks are broken down into smaller, manageable units.</li>
                        <li>Prioritise Tasks: Focus on critical path activities that directly impact the project deadline.</li>
                        <li>Update Schedule: Adjust timelines based on current progress and realistic estimates.</li>
                    </ul>
                </li>
                <li>
                    <strong>Improve Communication</strong><br>
                    <ul>
                        <li>Regular Updates: Hold frequent status meetings to track progress and identify issues early.</li>
                        <li>Clear Channels: Ensure there are clear communication channels among team members, stakeholders, and management.</li>
                    </ul>
                </li>
            </ol>
        `;

        responseMessageContainer.appendChild(botImage);
        responseMessageContainer.appendChild(responseMessageDiv);
        this.chatHistory.appendChild(responseMessageContainer);

        // Scroll to the bottom of chat history
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }

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

