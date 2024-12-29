# Voice-Redline Project Data Dictionary

## TABLE OF CONTENTS

1. [Backend (app/)](#backend-app)
   - [main.py](#mainpy)
     - [Classes](#classes)
     - [Endpoints](#endpoints)
   - [config.py](#configpy)
     - [Classes](#classes-1)
   - [services/](#services)
     - [ai_processor.py](#ai_processorpy)
     - [document_editor.py](#document_editorpy)
     - [command_handler.py](#command_handlerpy)
   - [utils/](#utils)
     - [audio.py](#audiopy)
     - [logging.py](#loggingpy)

2. [Chrome Extension (extension/)](#chrome-extension-extension)
   - [manifest.json](#manifestjson)
   - [oauth/](#oauth)
     - [config.js](#configjs)
     - [handler.js](#handlerjs)
   - [ui/](#ui)
     - [popup.html](#popuphtml)
     - [popup.js](#popupjs)
     - [styles.css](#stylescss)
   - [content/](#content)
     - [inject.js](#injectjs)
     - [commands.js](#commandsjs)

3. [Tests](#tests)
   - [tests/unit/](#testsunit)
     - [test_ai_processor.py](#test_ai_processorpy)
     - [test_document_editor.py](#test_document_editorpy)
     - [test_audio_utils.py](#test_audio_utilspy)
   - [tests/integration/](#testsintegration)
     - [test_api_endpoints.py](#test_api_endpointspy)
     - [test_websocket.py](#test_websocketpy)
   - [tests/e2e/](#testse2e)
     - [test_extension.py](#test_extensionpy)
     - [test_full_workflow.py](#test_full_workflowpy)
   - [tests/data/](#testsdata)
   - [tests/constants/](#testconstants)
     - [test_messages.py](#test_messagespy)
     - [message_loader.py](#message_loaderpy)

4. [Configuration](#configuration)
   - [.env](#env)
   - [requirements.txt](#requirementstxt)
   - [pyproject.toml](#pyprojecttoml)

5. [Documentation](#documentation)
   - [README.md](#readmemd)
   - [data_dictionary.md](#data_dictionarymd)
   - [project_structure.md](#project_structuremd)
   - [roadmap.md](#roadmapmd)

6. [Logs](#logs)
   - [logs/app.log](#logsapplog)
   - [logs/error.log](#logserrorlog)

## START OF DATA DICTIONARY

# Backend (app/)

## main.py

### Classes

#### ConnectionManager
- Purpose: Manages WebSocket connections and document sessions
- Attributes:
  - active_connections: List[WebSocket] - List of all active connections
  - document_sessions: Dict[str, List[WebSocket]] - Document-specific connections
- Methods:
  - connect(websocket: WebSocket, document_id: str) -> None
  - disconnect(websocket: WebSocket, document_id: str) -> None
  - broadcast_to_document(document_id: str, message: Dict) -> None

### Endpoints

#### GET /
- Purpose: Health check endpoint
- Returns: Dict with status and timestamp

#### POST /upload
- Purpose: Handle file uploads for processing
- Parameters:
  - file: UploadFile - The file to process
- Returns: Dict with processing results

#### WebSocket /ws/{document_id}
- Purpose: Handle real-time voice processing
- Parameters:
  - document_id: str - The document identifier

#### POST /process-command/{document_id}
- Purpose: Process manual commands
- Parameters:
  - document_id: str - The document identifier
  - command: Dict[str, Any] - The command to process

## config.py

### Classes

#### Settings
- Purpose: Application configuration management
- Attributes:
  - HOST: str - Server host address (default: "0.0.0.0")
  - PORT: int - Server port number (default: 8000)
  - LOG_LEVEL: str - Logging level (default: "INFO")
  - MAX_SUGGESTIONS: int - Maximum suggestions allowed
  - GROQ_API_KEY: str - API key for Groq
  - TESTING: bool - Testing mode flag

## services/

### ai_processor.py

#### Classes

##### AIProcessor
- Purpose: Processes text using Groq API for suggestions and commands
- Attributes:
  - client: groq.Client - Instance of Groq API client
  - is_listening: bool - Flag indicating if processor is listening
  - command_callback: Optional[Callable] - Callback for command processing

#### Methods
- start_listening(document_id: str) -> None
- stop_listening() -> None
- set_command_callback(callback: Callable) -> None
- handle_command(text: str) -> Dict[str, Any]
- process_input(data: bytes, input_type: str) -> Dict[str, Any]
- process_command(command: str) -> Dict[str, Any]
- get_suggestions(text: str) -> Dict[str, Any]
- generate_suggestions(text: str) -> dict
- handle_formatting(changes: dict) -> dict
- process_with_groq(text: str) -> dict

### document_editor.py

#### Classes

##### DocumentEditor
- Purpose: Manages document state and changes
- Attributes:
  - documents: Dict[str, Dict[str, Any]] - Document storage
  - document_states: Dict[str, str] - Document state tracking
  - change_history: Dict[str, List[Dict[str, Any]]] - Change history
  - ai_processor: AIProcessor - Instance of AI processor

#### Methods
- apply_changes(document_id: str, changes: Dict[str, Any]) -> Dict[str, Any]
- update_appendix(document_id: str, changes: Dict[str, Any]) -> None
- create_document(document_id: str, content: str) -> Dict[str, Any]
- get_document(document_id: str) -> Dict[str, Any]
- finalize_document(document_id: str) -> Dict[str, Any]
- restore_original(document_id: str) -> Dict[str, Any]
- _update_document_state(document_id: str, state: str) -> None
- _apply_document_changes(document: Dict, changes: Dict) -> Dict
- _apply_edit(content: str, new_text: str, position: int) -> str

### command_handler.py

#### Classes

##### CommandHandler
- Purpose: Processes voice and text commands
- Methods:
  - process_command(command: str) -> Dict
  - handle_voice_command(audio: bytes) -> Dict
  - validate_command(command: str) -> bool
  - execute_command(command: str) -> Dict[str, Any]
  - parse_command_parameters(command: str) -> Dict[str, Any]

## utils/

### audio.py

#### Functions
- validate_audio_format(audio_data: bytes) -> bool
- convert_audio_format(audio_data: bytes, target_format: Dict[str, Any]) -> bytes
- get_audio_duration(audio_data: bytes) -> float
- get_audio_properties(audio_data: bytes) -> Dict[str, Any]

### logging.py

#### Variables
- logger: logging.Logger - Application logger instance
- LOG_FORMAT: str - Log message format
- LOG_FILE: str - Log file path

#### Functions
- configure_logging() -> None
- log_error(message: str, error: Exception) -> None
- log_api_call(endpoint: str, method: str)


# Chrome Extension (extension/)

## manifest.json
- Purpose: Extension configuration file
- Properties:
  - manifest_version: int - Extension manifest version (3)
  - name: str - Extension name
  - version: str - Extension version
  - permissions: List[str] - Required browser permissions
    - activeTab
    - storage
    - identity
    - scripting
  - content_scripts: List[Dict] - Injected scripts configuration
  - background: Dict - Service worker configuration
  - icons: Dict - Extension icon paths

## oauth/

### config.js
- Purpose: OAuth configuration settings
- Variables:
  - CLIENT_ID: str - OAuth client identifier
  - AUTH_ENDPOINT: str - Authorization endpoint URL
  - TOKEN_ENDPOINT: str - Token endpoint URL
  - SCOPES: Array[str] - Required OAuth scopes

### handler.js
- Purpose: Authentication flow management
- Functions:
  - initializeAuth() -> Promise<void>
  - handleCallback(code: string) -> Promise<TokenResponse>
  - refreshToken() -> Promise<TokenResponse>
  - validateToken() -> boolean

## ui/

### popup.html
- Purpose: Extension popup interface structure
- Components:
  - Control buttons: Start/Stop recording
  - Status indicators: Connection status
  - Settings panel: Configuration options
  - Suggestion display: AI suggestions area

### popup.js
- Purpose: Popup interaction handling
- Functions:
  - initializePopup() -> void
  - handleCommands(command: string) -> Promise<void>
  - updateStatus(status: StatusType) -> void
  - displaySuggestions(suggestions: Array<Suggestion>) -> void

### styles.css
- Purpose: UI styling definitions
- Components:
  - Layout styles: Grid and flexbox layouts
  - Theme colors: Primary and secondary colors
  - Component styles: Buttons, panels, indicators

## content/

### inject.js
- Purpose: Document interaction script
- Functions:
  - injectMarkup(changes: Changes) -> void
  - handleSelection(range: Range) -> void
  - applyChanges(changes: Changes) -> void
  - trackChanges(mutation: MutationRecord) -> void

### commands.js
- Purpose: Voice command handlers
- Functions:
  - processVoiceCommand(audio: AudioData) -> Promise<Command>
  - executeCommand(command: Command) -> Promise<void>
  - updateUI(status: UIStatus) -> void

# Tests

## tests/unit/

### test_ai_processor.py
- Purpose: Unit tests for AI processing
- Test Cases:
  - test_command_processing() - Verify command interpretation
  - test_suggestion_generation() - Test AI suggestions
  - test_groq_integration() - Validate API integration

### test_document_editor.py
- Purpose: Unit tests for document editing
- Test Cases:
  - test_create_document() - Document creation
  - test_apply_changes() - Change application
  - test_version_control() - Version management

### test_audio_utils.py
- Purpose: Unit tests for audio processing
- Test Cases:
  - test_audio_validation() - Format validation
  - test_format_conversion() - Audio conversion
  - test_duration_calculation() - Duration computation

## tests/integration/

### test_api_endpoints.py
- Purpose: Integration tests for API endpoints
- Test Cases:
  - test_health_check() - API availability
  - test_document_upload() - File processing
  - test_command_processing() - Command handling

### test_websocket.py
- Purpose: Integration tests for WebSocket functionality
- Test Cases:
  - test_connection_lifecycle() - Connection management
  - test_document_sessions() - Session handling
  - test_real_time_updates() - Update propagation

## tests/e2e/

### test_extension.py
- Purpose: End-to-end tests for Chrome extension
- Test Cases:
  - test_extension_installation() - Installation flow
  - test_document_markup() - Markup functionality
  - test_voice_commands() - Voice control testing

### test_full_workflow.py
- Purpose: End-to-end tests for complete workflow
- Test Cases:
  - test_document_processing() - Full document flow
  - test_collaboration_flow() - Multi-user testing
  - test_error_handling() - Error recovery

## tests/data/
- Purpose: Test fixtures and sample data
- Contents:
  - sample_audio.wav - Test audio file
  - sample_document.txt - Test document
  - test_config.json - Test configuration

## tests/constants/

### test_messages.py
- Purpose: Define message types and their corresponding outputs
- Components:
  - MessageType (Enum): Standardized message types
    - Command messages (COMMAND_*)
    - Error messages (ERROR_*)
    - Success messages (SUCCESS_*)
  - MESSAGE_OUTPUTS (Dict): Mapping of message types to output strings
  - get_message(): Function to format messages with parameters

### message_loader.py
- Purpose: Load and format messages
- Methods:
  - get_message(message_type: MessageType, **kwargs) -> str

# Configuration

## .env
- Purpose: Environment variables
- Variables:
  - GROQ_API_KEY: str - API authentication key
  - HOST: str - Server host address
  - PORT: int - Server port number
  - LOG_LEVEL: str - Logging configuration

## requirements.txt
- Purpose: Python dependencies
- Categories:
  - Core dependencies
  - Development tools
  - Testing utilities

## pyproject.toml
- Purpose: Project configuration
- Settings:
  - Project metadata
  - Build system configuration
  - Tool settings
  - Test configurations

# Documentation

## README.md
- Purpose: Project overview and setup instructions
- Sections:
  - Project description
  - Installation steps
  - Usage guide
  - Configuration details

## data_dictionary.md
- Purpose: Term definitions and code documentation
- Sections:
  - Backend components
  - Extension components
  - Data structures
  - API endpoints

## project_structure.md
- Purpose: Directory layout documentation
- Sections:
  - Backend structure
  - Extension structure
  - Test organization
  - Configuration files

## roadmap.md
- Purpose: Development plan and milestones
- Sections:
  - Current features
  - Planned improvements
  - Release schedule
  - Known issues

# Logs

## logs/app.log
- Purpose: Application activity logging
- Contents:
  - Info level logs
  - Warning messages
  - Error traces
  - Request/response data

## logs/error.log
- Purpose: Error tracking
- Contents:
  - Error messages
  - Stack traces
  - Critical issues
  - System warnings