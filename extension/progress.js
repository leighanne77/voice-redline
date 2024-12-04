class ProgressManager {
    constructor() {
        this.activeOperations = new Map();
        this.createProgressUI();
    }

    createProgressUI() {
        this.progressContainer = document.createElement('div');
        this.progressContainer.className = 'progress-container';
        document.body.appendChild(this.progressContainer);
    }

    startOperation(operationType, options = {}) {
        const operationId = Date.now().toString();
        const progressElement = this.createProgressBar(operationType, options);
        
        this.activeOperations.set(operationId, {
            type: operationType,
            element: progressElement,
            progress: 0,
            options
        });

        return operationId;
    }

    updateProgress(operationId, progress, message = '') {
        const operation = this.activeOperations.get(operationId);
        if (!operation) return;

        operation.progress = Math.min(Math.max(progress, 0), 100);
        const progressBar = operation.element.querySelector('.progress-fill');
        const messageElement = operation.element.querySelector('.progress-message');

        // Animate progress
        progressBar.style.width = `${operation.progress}%`;
        
        // Update message if provided
        if (message) {
            messageElement.textContent = message;
        }

        // Complete operation if 100%
        if (operation.progress >= 100) {
            this.completeOperation(operationId);
        }
    }

    completeOperation(operationId) {
        const operation = this.activeOperations.get(operationId);
        if (!operation) return;

        operation.element.classList.add('complete');
        
        setTimeout(() => {
            operation.element.classList.add('fade-out');
            setTimeout(() => {
                operation.element.remove();
                this.activeOperations.delete(operationId);
            }, 300);
        }, 1000);
    }

    createProgressBar(type, options) {
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        progressBar.innerHTML = `
            <div class="progress-header">
                <div class="progress-type">${type}</div>
                <button class="progress-cancel">×</button>
            </div>
            <div class="progress-track">
                <div class="progress-fill"></div>
            </div>
            <div class="progress-message"></div>
        `;

        //
    }
} 