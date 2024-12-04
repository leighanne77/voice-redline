document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const clearButton = document.getElementById('clearButton');
    const acceptButton = document.getElementById('acceptButton');
    const acceptAllButton = document.getElementById('acceptAllButton');
    const suggestButton = document.getElementById('suggestButton');
    const moveCursorUpButton = document.getElementById('moveCursorUpButton');
    const moveCursorDownButton = document.getElementById('moveCursorDownButton');
    const statusDiv = document.getElementById('status');
    const transcriptDiv = document.getElementById('transcript');
    const suggestionsDiv = document.getElementById('suggestions');
    const previewPanel = document.getElementById('previewPanel');

    let isRecording = false;
    let socket = null;

    function updateButtonStates() {
        startButton.disabled = isRecording;
        stopButton.disabled = !isRecording;
        clearButton.disabled = !isRecording;
        acceptButton.disabled = !isRecording;
        suggestButton.disabled = !isRecording;
        moveCursorUpButton.disabled = !isRecording;
        moveCursorDownButton.disabled = !isRecording;
    }

    function updateStatus(message) {
        statusDiv.textContent = message;
    }

    function connectWebSocket() {
        socket = new WebSocket('ws://localhost:8000/ws');
        
        socket.onopen = function(event) {
            updateStatus('Connected to server');
        };
        
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            handleServerMessage(data);
        };
        
        socket.onclose = function(event) {
            updateStatus('Disconnected from server');
        };
    }

    function handleServerMessage(data) {
        switch(data.type) {
            case 'transcript':
                transcriptDiv.textContent = data.content;
                break;
            case 'suggestions':
                suggestionsDiv.textContent = data.content;
                break;
            case 'preview':
                previewPanel.innerHTML = data.content;
                break;
            case 'status':
                updateStatus(data.content);
                break;
        }
    }

    function sendMessage(action, data = {}) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({action, ...data}));
        } else {
            updateStatus('Not connected to server');
        }
    }

    startButton.addEventListener('click', function() {
        sendMessage('startRecognition');
        isRecording = true;
        updateButtonStates();
        updateStatus('Voice recognition started');
    });

    stopButton.addEventListener('click', function() {
        sendMessage('stopRecognition');
        isRecording = false;
        updateButtonStates();
        updateStatus('Voice recognition stopped');
    });

    clearButton.addEventListener('click', function() {
        sendMessage('clearChanges');
    });

    acceptButton.addEventListener('click', function() {
        sendMessage('acceptChanges');
    });

    acceptAllButton.addEventListener('click', function() {
        sendMessage('acceptAllChanges');
    });

    suggestButton.addEventListener('click', function() {
        sendMessage('getSuggestions');
    });

    moveCursorUpButton.addEventListener('click', function() {
        sendMessage('moveCursor', {direction: 'up'});
    });

    moveCursorDownButton.addEventListener('click', function() {
        sendMessage('moveCursor', {direction: 'down'});
    });

    function handleVoiceCommand(command) {
        switch(command.toLowerCase()) {
            case 'start redlining':
                startButton.click();
                break;
            case 'stop redlining':
                stopButton.click();
                break;
            case 'clear markup':
                clearButton.click();
                break;
            case 'accept suggested':
                acceptButton.click();
                break;
            case 'accept all, move to final':
                acceptAllButton.click();
                break;
            case 'move cursor up':
                moveCursorUpButton.click();
                break;
            case 'move cursor down':
                moveCursorDownButton.click();
                break;
            case 'go forward':
                sendMessage('moveCursor', {direction: 'forward'});
                break;
            case 'go forward two':
                sendMessage('moveCursor', {direction: 'forward', steps: 2});
                break;
            case 'make suggestion':
                suggestButton.click();
                break;
            default:
                if (command.startsWith('move cursor to the words')) {
                    const words = command.split('move cursor to the words')[1].trim();
                    sendMessage('moveCursorToWords', {words});
                } else {
                    updateStatus(`Unrecognized voice command: ${command}`);
                }
        }
    }

    // Initialize WebSocket connection
    connectWebSocket();
});