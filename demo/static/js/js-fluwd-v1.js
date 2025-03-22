class ChatApp {
  constructor() {
    // DOM elements
    this.chatForm = document.getElementById('chat-form');
    this.chatInput = document.getElementById('chat-input');
    this.messages = document.getElementById('messages');
    this.welcomeCard = document.querySelector('.welcome-card');
    this.featureContainer = document.querySelector('.feature-container');
    this.chatContainer = document.querySelector('.chat-container');
    
    // Bind methods to preserve 'this' context
    this.handleSubmit = this.handleSubmit.bind(this);
    this.scrollToBottom = this.scrollToBottom.bind(this);
    
    // Initialize event listeners
    this.initEventListeners();
    
    // Ensure chat starts at the bottom on load
    setTimeout(this.scrollToBottom, 100);
  }
  
  initEventListeners() {
    // Handle form submission
    this.chatForm.addEventListener('submit', this.handleSubmit);
    
    // Add window load event for initial scroll
    window.addEventListener('load', () => {
      setTimeout(this.scrollToBottom, 200);
    });
  }
  
  handleSubmit(e) {
    e.preventDefault();
    
    const message = this.chatInput.value.trim();
    if (!message) return;
    
    // Add user message
    this.addUserMessage(message);
    
    // Transition from welcome screen to chat
    this.transitionToChatView(() => {
      // Show bot typing indicator
      this.showBotTyping();
      
      // Get response (with potential for async processing)
      this.processBotResponse(message);
    });
    
    // Clear input
    this.chatInput.value = '';
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
    messageDiv.innerHTML = `
      <div class="user-message">${this.sanitizeHTML(message)}</div>
      <div class="user-icon">
        <i class="fas fa-user"></i>
      </div>
    `;
    this.messages.appendChild(messageDiv);
    setTimeout(this.scrollToBottom, 50);
  }
  
  addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-wrapper bot-container';
    messageDiv.innerHTML = `
      <div class="bot-icon">
        <i class="fas fa-robot"></i>
      </div>
      <div class="bot-message">${message}</div>
    `;
    this.messages.appendChild(messageDiv);
    setTimeout(this.scrollToBottom, 50);
  }
  
  showBotTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message-wrapper bot-container';
    typingDiv.id = 'bot-typing';
    typingDiv.innerHTML = `
      <div class="bot-icon">
        <i class="fas fa-robot"></i>
      </div>
      <div class="bot-message bot-typing">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    `;
    this.messages.appendChild(typingDiv);
    this.scrollToBottom();
  }
  
  hideBotTyping() {
    const typingDiv = document.getElementById('bot-typing');
    if (typingDiv) {
      typingDiv.remove();
    }
  }
  
  processBotResponse(message) {
    // Simulate API call or processing delay
    setTimeout(() => {
      this.hideBotTyping();
      const response = this.getBotResponse(message);
      this.addBotMessage(response);
    }, 1500 + Math.random() * 1000); // Varied response time for realism
  }
  
  getBotResponse(message) {
    // Enhanced response handling
    const lowercaseMsg = message.toLowerCase();
    
    if (lowercaseMsg.includes('delayed project schedule')) {
      return `
        <p><strong>Here are steps to address your delayed project schedule:</strong></p>
        <ol>
          <li><strong>Analyze the root cause</strong> - Identify specific bottlenecks and dependencies causing delays.</li>
          <li><strong>Update the critical path</strong> - Re-evaluate task dependencies and identify which delayed tasks are affecting the timeline most severely.</li>
          <li><strong>Resource reallocation</strong> - Consider temporarily shifting resources from non-critical tasks to expedite critical path items.</li>
          <li><strong>Adjust scope if necessary</strong> - Evaluate whether some deliverables can be adjusted or phased differently to meet critical deadlines.</li>
          <li><strong>Communicate transparently</strong> - Update stakeholders with the revised timeline and mitigation plan.</li>
        </ol>
        <p>Would you like me to help you implement any of these strategies? I can create a detailed recovery plan or help you communicate with stakeholders.</p>
      `;
    } else if (lowercaseMsg.includes('hello') || lowercaseMsg.includes('hi')) {
      return 'Hello! How can I assist you with your project management today?';
    } else if (lowercaseMsg.includes('thank')) {
      return 'You\'re welcome! Is there anything else you need help with?';
    } else {
      return `I'll help you with that. What specific information do you need about "${this.sanitizeHTML(message)}"?`;
    }
  }
  
  scrollToBottom() {
    requestAnimationFrame(() => {
      this.messages.scrollTop = this.messages.scrollHeight;
    });
  }
  
  // Security improvement - sanitize input to prevent XSS
  sanitizeHTML(text) {
    const element = document.createElement('div');
    element.textContent = text;
    return element.innerHTML;
  }
}

