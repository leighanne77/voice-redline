let isRecognitionActive = false;

// OAuth token management
let authToken = null;

// Function to get OAuth token
async function getAuthToken() {
  return new Promise((resolve, reject) => {
    chrome.identity.getAuthToken({ interactive: true }, function(token) {
      if (chrome.runtime.lastError) {
        console.error('OAuth Error:', chrome.runtime.lastError);
        reject(chrome.runtime.lastError);
        return;
      }
      authToken = token;
      chrome.storage.local.set({ 'oauth_token': token });
      resolve(token);
    });
  });
}

// Function to check if token is valid
async function validateToken() {
  if (!authToken) {
    try {
      authToken = await getAuthToken();
    } catch (error) {
      console.error('Failed to get auth token:', error);
      return false;
    }
  }
  return true;
}

// Message handling
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // OAuth token request
  if (request.type === 'GET_AUTH_TOKEN') {
    getAuthToken()
      .then(token => sendResponse({ token }))
      .catch(error => sendResponse({ error: error.message }));
    return true;
  }

  // Voice command processing
  if (request.type === 'PROCESS_VOICE') {
    validateToken().then(isValid => {
      if (!isValid) {
        sendResponse({ error: 'Authentication failed' });
        return;
      }
      // Process voice command with token
      processVoiceCommand(request.data, authToken)
        .then(result => sendResponse(result))
        .catch(error => sendResponse({ error: error.message }));
    });
    return true;
  }

  // Start recognition
  if (request.action === "startRecognition") {
    isRecognitionActive = true;
    // Here we would typically start the connection to our Python backend
    // For now, we'll just respond that it's started
    sendResponse({status: "started"});
  } else if (request.action === "stopRecognition") {
    isRecognitionActive = false;
    // Here we would typically stop the connection to our Python backend
    // For now, we'll just respond that it's stopped
    sendResponse({status: "stopped"});
  }
  return true;  // Indicates that we will respond asynchronously
});

// This is where we would handle incoming messages from the Python backend
// and send them to the content script for highlighting
function handleBackendMessage(message) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {
            action: "highlight",
            text: message.text
        });
    });
}