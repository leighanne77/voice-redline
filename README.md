#extension is under construction will be updated Jan 1, 2025
# Real-Time Collaborative Document Markup Tool

This tool uses the Groq API and is a Chrome Browser Extension, allowing you to mark up and change online documents, including Google Documents and Microsoft Documents, paragraph-by-paragraph with the help of a pop up side panel, right in your browser. The tool responds to manual and voice-enabled commands, and makes suggestions in the pop up preview panel, paragraph-by-paragraph. 

## Running the Application

1. Ensure your virtual environment is activated. If not, activate it using the commands in step 2 of the Installation section.

2. Start the voice processing server:
   ```
   cd src
   python voice_processor.py
   ```

3. The voice processing server will start running on `ws://localhost:8765`

4. Start the main backend server:
   ```
   python main.py
   ```

5. The main server will start running on `http://localhost:8000`

6. Use the browser extension as described in the Usage section below.

To deactivate the virtual environment when you're done, simply run:
```
deactivate
```
## Usage

1. Start both the voice processing server and the main backend server as described in the "Running the Application" section.

2. Use the browser extension for collaborative document editing:
   - Open a document in Google Docs or Microsoft Office Online
   - Click on the extension icon in your browser
   - Grant necessary permissions for audio capture and document access
   - Move the cursor to where you need to start making changes
   - Use the following controls in the extension popup to start your collaborative editing session
Manual:
  - Start Redlining
  - Stop Redlining
  - Make New Suggestions
  - Accept Suggestion
  - Clear
  - Accept All
- Voice command detection and processing:
  - "start redlining"
  - "stop redlining"
  - "move cursor up"
  - "move cursor down"
  - "go forward"
  - "go forward two"
  - "move cursor to the words ____"
  - "make suggestion"
  - "Accept Suggested"
  - "Clear markup, restore original"
  - "Accept All, Move to Final"
- The tool will have visual highlighting of changes in the document
- And a preview panel for suggestions "Start" to begin capturing the conversation or use the voice command
     * As you and your collaborators discuss changes, the extension will:
       - Capture the conversation in real-time using WebSocket communication, but not transcribe until the "start redlining" command or manual commands are used
       - Analyze the entire document for relevant markup suggestions
       - Apply changes to the document in real-time whenever the "start redlining" or manual "start" button is ued
       - Keep original text after the new text, but with the font strikout
       - Highlight the new text, the changes, visually in the document
     * Click "Stop" to pause the audio capture or say "stop redlining"
     * Use the "Clear Changes" button to reset the current set of suggestions and highlights, or say "clear markup, restore original"
     * Click "Accept Changes" to finalize all the markup texts in the document, or say "Accept All, Move to Final"

     All changes will be logged and tracked in an appendix at the end of the document, even after "Accept Changes" is pressed or the words "Accept All, Move to Final" are said

  

## Project Structure

- `src/`: Contains the backend code
  - `main.py`: FastAPI application setup
  - `voice_processor.py`: Handles speech-to-text conversion and WebSocket communication for real-time audio processing
  - `ai_processor.py`: Processes text using Groq API for markup suggestions
  - `document_editor.py`: Manages real-time document edits
  - `config.py`: Manages configuration settings
  - `test_collaborative_markup.py`: Script for testing the collaborative markup functionality
- `extension/`: Contains the browser extension code for Google Docs and Microsoft Office Online integration
- `requirements.txt`: List of Python dependencies
- `.env`: Configuration file for storing API keys (not tracked in git)

Second Priority: Edge Cases Handled: 


## Appendix: Edge Cases

First Priority: 

### UI/UX
- Too many suggestions
- Very long suggestions
- Special formatting in suggestions
- Panel size constraints
- Display overflow
- Formatting preservation


### Voice Commands
- Background noise/unclear speech
- Multiple commands in one transcript
- Similar sounding commands
- Partial/incomplete commands
- Low confidence scores
- Ambiguous commands

### Real-time Synchronization
- Multiple users editing same paragraph
- Network interruptions
- Out-of-order updates
- Failed suggestions
- Conflicting edits
- Connection drops

Second Priority:

### Document Structure
- Empty paragraphs
- Cursor in lists/tables/special elements
- Cursor in comments or suggestions
- Nested content structures
- Missing editor element (when page is loading, unsupported document type, or DOM structure changes)
- No selection range found

### Content Processing
- Empty or whitespace-only text
- Text exceeding maximum length
- Special characters and formatting
- Multiple languages in one document
- Malformed paragraph structures
- Invalid text content
