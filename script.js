class NLPChatbot {
    constructor() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.themeToggle = document.getElementById('theme-toggle');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.quickActions = document.querySelectorAll('.quick-action');
        
        // Backend API URL
        this.apiBaseUrl = 'http://localhost:5000';
        
        this.initializeTheme();
        this.initializeEventListeners();
        this.checkBackendConnection();
    }
    
    initializeTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateThemeIcon(savedTheme);
    }
    
    updateThemeIcon(theme) {
        const icon = this.themeToggle.querySelector('i');
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    initializeEventListeners() {
        this.sendButton.addEventListener('click', () => this.handleUserInput());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleUserInput();
            }
        });
        
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        this.quickActions.forEach(button => {
            button.addEventListener('click', () => {
                const message = button.getAttribute('data-message');
                this.userInput.value = message;
                this.handleUserInput();
            });
        });
    }
    
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        this.updateThemeIcon(newTheme);
    }
    
    async checkBackendConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            console.log('✅ Backend connected:', data);
            this.backendAvailable = true;
            this.showConnectionStatus('Connected to Python backend', 'success');
        } catch (error) {
            console.warn('⚠️ Backend not available, using fallback mode:', error);
            this.backendAvailable = false;
            this.initializeFallbackResponses();
            this.showConnectionStatus('Backend offline - Using fallback mode', 'warning');
        }
    }
    
    showConnectionStatus(message, type) {
        // Create or update connection status indicator
        let statusDiv = document.getElementById('connection-status');
        if (!statusDiv) {
            statusDiv = document.createElement('div');
            statusDiv.id = 'connection-status';
            statusDiv.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                z-index: 1000;
                transition: all 0.3s ease;
            `;
            document.body.appendChild(statusDiv);
        }
        
        statusDiv.textContent = message;
        if (type === 'success') {
            statusDiv.style.background = 'linear-gradient(135deg, #48bb78, #38a169)';
            statusDiv.style.color = 'white';
        } else {
            statusDiv.style.background = 'linear-gradient(135deg, #ed8936, #dd6b20)';
            statusDiv.style.color = 'white';
        }
        
        // Hide after 3 seconds
        setTimeout(() => {
            statusDiv.style.opacity = '0';
            setTimeout(() => statusDiv.remove(), 300);
        }, 3000);
    }
    
    initializeFallbackResponses() {
        this.fallbackResponses = {
            greetings: [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Hey! How are you doing today?"
            ],
            default: [
                "I'm currently in fallback mode. The Python backend is not running. Please start the backend server for advanced NLP features.",
                "The Python backend is not available. Please run 'python app.py' to enable advanced features.",
                "Backend connection failed. Please ensure the Flask server is running on localhost:5000."
            ]
        };
    }
    
    async processNLP(input) {
        if (this.backendAvailable) {
            try {
                const response = await fetch(`${this.apiBaseUrl}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: input })
                });
                
                if (!response.ok) {
                    throw new Error('Backend request failed');
                }
                
                const data = await response.json();
                return data;
            } catch (error) {
                console.warn('Backend request failed, using fallback:', error);
                return { response: this.getFallbackResponse(input), sentiment: 'neutral' };
            }
        } else {
            return { response: this.getFallbackResponse(input), sentiment: 'neutral' };
        }
    }
    
    getFallbackResponse(input) {
        const text = input.toLowerCase().trim();
        
        if (text.includes('hello') || text.includes('hi') || text.includes('hey')) {
            return this.fallbackResponses.greetings[Math.floor(Math.random() * this.fallbackResponses.greetings.length)];
        }
        
        return this.fallbackResponses.default[Math.floor(Math.random() * this.fallbackResponses.default.length)];
    }
    
    async handleUserInput() {
        const input = this.userInput.value.trim();
        if (!input) return;
        
        this.addMessage(input, 'user');
        this.userInput.value = '';
        
        this.showTypingIndicator();
        
        try {
            const response = await this.processNLP(input);
            this.hideTypingIndicator();
            this.addMessage(response.response, 'bot', response);
        } catch (error) {
            this.hideTypingIndicator();
            console.error('Error processing message:', error);
            this.addMessage("Sorry, I encountered an error while processing your message.", 'bot');
        }
    }
    
    addMessage(content, sender, sentimentData = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user' 
            ? '<i class="fas fa-user"></i>' 
            : '<i class="fas fa-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const paragraph = document.createElement('p');
        paragraph.textContent = content;
        contentDiv.appendChild(paragraph);
        
        // Add sentiment indicator for bot messages when backend is available
        if (sender === 'bot' && sentimentData && sentimentData.sentiment && this.backendAvailable) {
            const sentimentDiv = document.createElement('div');
            sentimentDiv.className = 'sentiment-indicator';
            sentimentDiv.style.cssText = `
                font-size: 11px;
                margin-top: 5px;
                padding: 2px 6px;
                border-radius: 10px;
                display: inline-block;
                opacity: 0.8;
            `;
            
            const sentiment = sentimentData.sentiment;
            const confidence = sentimentData.confidence || 0;
            
            if (sentiment === 'positive') {
                sentimentDiv.style.background = 'linear-gradient(135deg, #48bb78, #38a169)';
                sentimentDiv.style.color = 'white';
                sentimentDiv.innerHTML = `😊 Positive ${Math.round(confidence * 100)}%`;
            } else if (sentiment === 'negative') {
                sentimentDiv.style.background = 'linear-gradient(135deg, #f56565, #e53e3e)';
                sentimentDiv.style.color = 'white';
                sentimentDiv.innerHTML = `😔 Negative ${Math.round(confidence * 100)}%`;
            } else {
                sentimentDiv.style.background = 'linear-gradient(135deg, #718096, #4a5568)';
                sentimentDiv.style.color = 'white';
                sentimentDiv.innerHTML = `😐 Neutral ${Math.round(confidence * 100)}%`;
            }
            
            contentDiv.appendChild(sentimentDiv);
        }
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.typingIndicator.classList.add('active');
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.classList.remove('active');
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new NLPChatbot();
});

document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        document.getElementById('user-input').focus();
    }
});

window.addEventListener('load', () => {
    document.getElementById('user-input').focus();
});
