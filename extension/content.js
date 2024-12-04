// Content script for Voice Redline

// Initialize state
let isRecording = false;
let currentDocumentId = null;
let websocket = null;

// Get document ID from URL
function getDocumentId() {
    const match = window.location.pathname.match(/\/document\/d\/([^/]+)/);
    return match ? match[1] : null;
}

// Initialize Google Docs integration
async function initializeGoogleDocs() {
    try {
        const response = await chrome.runtime.sendMessage({ type: 'GET_AUTH_TOKEN' });
        if (response.error) {
            throw new Error(response.error);
        }
        
        currentDocumentId = getDocumentId();
        if (!currentDocumentId) {
            throw new Error('No document ID found');
        }

        console.log('Voice Redline: Initialized for document', currentDocumentId);
        return true;
    } catch (error) {
        console.error('Voice Redline: Initialization failed:', error);
        return false;
    }
}

// WebSocket connection management
function connectWebSocket() {
    try {
        websocket = new WebSocket('ws://localhost:8000/ws/' + currentDocumentId);
        
        websocket.onopen = () => {
            console.log('Voice Redline: WebSocket connected');
            updateUI('connected');
        };

        websocket.onmessage = async (event) => {
            const data = JSON.parse(event.data);
            await handleWebSocketMessage(data);
        };

        websocket.onclose = () => {
            console.log('Voice Redline: WebSocket disconnected');
            updateUI('disconnected');
            setTimeout(connectWebSocket, 5000); // Reconnect after 5 seconds
        };

        websocket.onerror = (error) => {
            console.error('Voice Redline: WebSocket error:', error);
            updateUI('error');
        };
    } catch (error) {
        console.error('Voice Redline: WebSocket connection failed:', error);
    }
}

// Handle WebSocket messages
async function handleWebSocketMessage(data) {
    try {
        if (data.type === 'document_update') {
            await applyDocumentChanges(data.changes);
        } else if (data.type === 'suggestion') {
            showSuggestion(data.content);
        } else if (data.type === 'error') {
            showError(data.message);
        }
    } catch (error) {
        console.error('Voice Redline: Error handling message:', error);
    }
}

// Apply changes to document
async function applyDocumentChanges(changes) {
    try {
        const response = await chrome.runtime.sendMessage({
            type: 'EDIT_DOCUMENT',
            data: {
                documentId: currentDocumentId,
                changes: changes
            }
        });

        if (response.error) {
            throw new Error(response.error);
        }

        console.log('Voice Redline: Changes applied successfully');
    } catch (error) {
        console.error('Voice Redline: Error applying changes:', error);
        showError('Failed to apply changes');
    }
}

// UI updates
function updateUI(status) {
    const icon = document.getElementById('voice-redline-icon');
    if (icon) {
        icon.className = `voice-redline-icon ${status}`;
    }
}

function showSuggestion(content) {
    // Create or update suggestion UI
    const suggestionEl = document.getElementById('voice-redline-suggestion') || 
                        createSuggestionElement();
    suggestionEl.textContent = content;
    suggestionEl.style.display = 'block';
}

function showError(message) {
    console.error('Voice Redline Error:', message);
    // Update UI to show error state
    updateUI('error');
}

// Create UI elements
function createSuggestionElement() {
    const el = document.createElement('div');
    el.id = 'voice-redline-suggestion';
    el.className = 'voice-redline-suggestion';
    document.body.appendChild(el);
    return el;
}

// Initialize extension
async function initialize() {
    try {
        const initialized = await initializeGoogleDocs();
        if (initialized) {
            connectWebSocket();
            injectUI();
            console.log('Voice Redline: Extension initialized successfully');
        }
    } catch (error) {
        console.error('Voice Redline: Initialization error:', error);
    }
}

// Inject UI elements
function injectUI() {
    const container = document.createElement('div');
    container.id = 'voice-redline-container';
    container.innerHTML = `
        <div id="voice-redline-icon" class="voice-redline-icon"></div>
        <div id="voice-redline-controls">
            <button id="voice-redline-toggle">Start Recording</button>
        </div>
    `;
    document.body.appendChild(container);

    // Add event listeners
    document.getElementById('voice-redline-toggle').addEventListener('click', toggleRecording);
}

// Toggle recording state
async function toggleRecording() {
    try {
        isRecording = !isRecording;
        const button = document.getElementById('voice-redline-toggle');
        button.textContent = isRecording ? 'Stop Recording' : 'Start Recording';
        
        await chrome.runtime.sendMessage({
            type: 'PROCESS_VOICE',
            data: {
                action: isRecording ? 'start' : 'stop',
                documentId: currentDocumentId
            }
        });

        updateUI(isRecording ? 'recording' : 'connected');
    } catch (error) {
        console.error('Voice Redline: Recording toggle error:', error);
        showError('Failed to toggle recording');
    }
}

// Start initialization when document is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}