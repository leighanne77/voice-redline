class ShortcutManager {
    constructor(documentManager) {
        this.documentManager = documentManager;
        this.shortcuts = new Map();
        this.setupDefaultShortcuts();
        this.createQuickActionBar();
    }

    setupDefaultShortcuts() {
        document.addEventListener('keydown', (e) => {
            const shortcutKey = this.getShortcutKey(e);
            const action = this.shortcuts.get(shortcutKey);
            
            if (action) {
                e.preventDefault();
                action();
            }
        });

        // Add default shortcuts
        this.addShortcut('Ctrl+Shift+V', () => {
            this.documentManager.toggleVoiceRecognition();
        });

        this.addShortcut('Ctrl+Shift+Z', () => {
            this.documentManager.undoLastChange();
        });

        this.addShortcut('Ctrl+Shift+A', () => {
            this.documentManager.acceptAllChanges();
        });
    }

    getShortcutKey(event) {
        const keys = [];
        if (event.ctrlKey) keys.push('Ctrl');
        if (event.shiftKey) keys.push('Shift');
        if (event.altKey) keys.push('Alt');
        if (event.key !== 'Control' && event.key !== 'Shift' && event.key !== 'Alt') {
            keys.push(event.key.toUpperCase());
        }
        return keys.join('+');
    }

    addShortcut(keys, callback) {
        this.shortcuts.set(keys, callback);
    }

    createQuickActionBar() {
        const actionBar = document.createElement('div');
        actionBar.className = 'quick-action-bar';
        actionBar.innerHTML = `
            <button title="Start/Stop Voice (Ctrl+Shift+V)" class="action-btn voice-btn"></button>
            <button title="Accept Changes (Ctrl+Shift+A)" class="action-btn accept-btn">✓</button>
            <button title="Reject Changes" class="action-btn reject-btn">✗</button>
            <button title="Show History" class="action-btn history-btn">📋</button>
        `;

        // Add event listeners
        actionBar.querySelector('.voice-btn').onclick = () => 
            this.documentManager.toggleVoiceRecognition();
        actionBar.querySelector('.accept-btn').onclick = () => 
            this.documentManager.acceptAllChanges();
        actionBar.querySelector('.reject-btn').onclick = () => 
            this.documentManager.rejectAllChanges();
        actionBar.querySelector('.history-btn').onclick = () => 
            this.documentManager.showHistory();

        document.body.appendChild(actionBar);
    }
}

window.ShortcutManager = ShortcutManager; 