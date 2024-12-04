class UserFeedbackManager {
    constructor() {
        this.initializeUI();
        this.commandHistory = [];
        this.statusTimeout = null;
    }

    initializeUI() {
        // Status bubble
        this.statusBubble = document.createElement('div');
        this.statusBubble.className = 'voice-redline-status';
        this.statusBubble.style.display = 'none';
        document.body.appendChild(this.statusBubble);

        // Feedback panel
        this.feedbackPanel = document.createElement('div');
        this.feedbackPanel.className = 'voice-redline-feedback';
        document.body.appendChild(this.feedbackPanel);

        // Initialize with ready state
        this.showStatus('ready');
    }

    showStatus(status, duration = 3000) {
        clearTimeout(this.statusTimeout);
        this.statusBubble.style.display = 'flex';

        switch(status) {
            case 'listening':
                this.statusBubble.innerHTML = `
                    <div class="pulse-dot"></div>
                    <span>Listening...</span>
                `;
                break;
            case 'processing':
                this.statusBubble.innerHTML = `
                    <div class="spinner"></div>
                    <span>Processing...</span>
                `;
                break;
            case 'ready':
                this.statusBubble.innerHTML = `
                    <div class="check-mark"></div>
                    <span>Ready</span>
                `;
                break;
            case 'error':
                this.statusBubble.innerHTML = `
                    <div class="error-mark"></div>
                    <span>Error</span>
                `;
                break;
        }

        if (duration) {
            this.statusTimeout = setTimeout(() => {
                this.statusBubble.style.display = 'none';
            }, duration);
        }
    }

    showCommandFeedback(command, status = 'success') {
        this.commandHistory.push({
            command,
            status,
            timestamp: Date.now()
        });

        const feedback = document.createElement('div');
        feedback.className = `command-feedback ${status}`;
        feedback.innerHTML = `
            <span class="command-text">${command}</span>
            <span class="command-status">${status === 'success' ? '✓' : '✗'}</span>
        `;
        
        this.feedbackPanel.appendChild(feedback);
        
        // Animate and remove after delay
        requestAnimationFrame(() => {
            feedback.style.opacity = '1';
            feedback.style.transform = 'translateX(0)';
        });

        setTimeout(() => {
            feedback.style.opacity = '0';
            feedback.style.transform = 'translateX(100%)';
            setTimeout(() => feedback.remove(), 300);
        }, 3000);
    }
}

// Export for use in other files
window.UserFeedbackManager = UserFeedbackManager; 