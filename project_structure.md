# Project Structure

## Backend (app/)
- **main.py**: FastAPI application entry point
- **config.py**: Configuration and environment settings
- **services/**
  - **ai_processor.py**: Groq API integration
  - **command_handler.py**: Voice command processing
  - **document_editor.py**: Document manipulation
- **utils/**
  - **logging.py**: Logging configuration
  - **audio.py**: Audio processing utilities

## Chrome Extension (extension/)
- **manifest.json**: Extension configuration
- **oauth/**
  - **config.js**: OAuth configuration
  - **handler.js**: Authentication flow
- **ui/**
  - **popup.html**: Extension popup interface
  - **popup.js**: Popup interactions
  - **styles.css**: UI styling
- **content/**
  - **inject.js**: Document interaction script
  - **commands.js**: Voice command handlers

## Tests
- **tests/**
  - **unit/**: Unit test cases
  - **integration/**: Integration tests
  - **e2e/**: End-to-end tests
  - **data/**: Test data and fixtures
  - **conftest.py**: Test configuration

## Configuration
- **.env**: Environment variables
- **requirements.txt**: Python dependencies
- **pyproject.toml**: Project configuration
- **update_imports.py**: Import path management

## Documentation
- **README.md**: Project overview
- **data_dictionary.md**: Term definitions
- **project_structure.md**: Directory layout
- **roadmap.md**: Development plan
- **todos.txt**: Current tasks

## Logs
- **logs/**
  - **app.log**: Application logs
  - **error.log**: Error tracking