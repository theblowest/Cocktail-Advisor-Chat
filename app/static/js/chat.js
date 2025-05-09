document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const suggestionButtons = document.querySelectorAll('.suggestion');
    
    // Chat history for context
    let chatHistory = [];
    
    // Add event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Add event listeners to suggestion buttons
    suggestionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.getAttribute('data-message');
            userInput.value = message;
            sendMessage();
        });
    });
    
    // Function to send message
    function sendMessage() {
        const message = userInput.value.trim();
        
        // Don't send empty messages
        if (!message) return;
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        // Clear input
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Add to chat history
        chatHistory.push({
            role: 'user',
            content: message
        });
        
        // Send message to API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add assistant message to chat
            addMessageToChat('assistant', data.message, data.sources);
            
            // Add to chat history
            chatHistory.push({
                role: 'assistant',
                content: data.message
            });
            
            // Keep chat history manageable (limit to last 10 exchanges)
            if (chatHistory.length > 20) {
                chatHistory = chatHistory.slice(-20);
            }
            
            // Scroll to bottom
            scrollToBottom();
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Remove typing indicator
            removeTypingIndicator();
            
            // Show error message
            addMessageToChat('assistant', 'Sorry, there was an error processing your request. Please try again.');
        });
    }
    
    // Function to add message to chat
    function addMessageToChat(role, content, sources = null) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', role);
        
        const avatarElement = document.createElement('div');
        avatarElement.classList.add('avatar');
        
        const avatarIcon = document.createElement('i');
        avatarIcon.classList.add('fas', role === 'user' ? 'fa-user' : 'fa-robot');
        
        avatarElement.appendChild(avatarIcon);
        
        const contentElement = document.createElement('div');
        contentElement.classList.add('content');
        
        // Process content (handle paragraphs and formatting)
        const formattedContent = formatMessageContent(content);
        contentElement.innerHTML = formattedContent;
        
        // Add sources if available
        if (sources && sources.length > 0) {
            const sourcesElement = document.createElement('div');
            sourcesElement.classList.add('sources');
            sourcesElement.textContent = 'Sources: ' + sources.join(', ');
            contentElement.appendChild(sourcesElement);
        }
        
        messageElement.appendChild(avatarElement);
        messageElement.appendChild(contentElement);
        
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    // Function to format message content
    function formatMessageContent(content) {
        // Replace newlines with <br>
        let formatted = content.replace(/\n/g, '<br>');
        
        // Handle code blocks (if any)
        formatted = formatted.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        
        // Handle bullet points
        formatted = formatted.replace(/^\* (.+)$/gm, '<li>$1</li>');
        formatted = formatted.replace(/(<li>.+<\/li>)+/g, '<ul>$&</ul>');
        
        // Handle numbered lists
        formatted = formatted.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
        formatted = formatted.replace(/(<li>.+<\/li>)+/g, '<ol>$&</ol>');
        
        // Handle bold text
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formatted = formatted.replace(/__(.*?)__/g, '<strong>$1</strong>');
        
        // Handle italic text
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
        formatted = formatted.replace(/_(.*?)_/g, '<em>$1</em>');
        
        // Split into paragraphs if no HTML tags are present
        if (!/<[a-z][\s\S]*>/i.test(formatted)) {
            const paragraphs = formatted.split('<br><br>');
            formatted = paragraphs.map(p => `<p>${p.replace(/<br>/g, ' ')}</p>`).join('');
        }
        
        return formatted;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const indicatorElement = document.createElement('div');
        indicatorElement.classList.add('message', 'assistant', 'typing-indicator-container');
        
        const avatarElement = document.createElement('div');
        avatarElement.classList.add('avatar');
        
        const avatarIcon = document.createElement('i');
        avatarIcon.classList.add('fas', 'fa-robot');
        
        avatarElement.appendChild(avatarIcon);
        
        const contentElement = document.createElement('div');
        contentElement.classList.add('content');
        
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        
        contentElement.appendChild(typingIndicator);
        
        indicatorElement.appendChild(avatarElement);
        indicatorElement.appendChild(contentElement);
        
        chatMessages.appendChild(indicatorElement);
        
        scrollToBottom();
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const indicatorElement = document.querySelector('.typing-indicator-container');
        if (indicatorElement) {
            indicatorElement.remove();
        }
    }
    
    // Function to scroll to bottom of chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});