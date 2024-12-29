# Dependencies Documentation

## Core Dependencies

### FastAPI Framework
- **Package**: `fastapi==0.104.0`
- **Purpose**: Main web framework for building APIs
- **Usage**: Routes, WebSocket handling, request/response management

### Uvicorn
- **Package**: `uvicorn==0.24.0`
- **Purpose**: ASGI server implementation
- **Usage**: Serving the FastAPI application

### WebSockets
- **Package**: `websockets==12.0`
- **Purpose**: WebSocket protocol implementation
- **Usage**: Real-time voice data streaming

### Pydantic
- **Package**: `pydantic==2.4.2`
- **Purpose**: Data validation using Python type annotations
- **Usage**: Request/response models, configuration management

## Audio Processing

### Speech Recognition
- **Package**: `SpeechRecognition==3.10.0`
- **Purpose**: Converting speech to text
- **Usage**: Processing voice commands

## AI Integration

### Groq
- **Package**: `groq==0.4.0`
- **Purpose**: AI model integration
- **Usage**: Processing text commands and generating suggestions

## Development Tools

### Code Formatting
- **Package**: `black==23.10.0`
- **Purpose**: Code formatting
- **Usage**: `black .` to format code
- **Package**: `isort==5.12.0`
- **Purpose**: Import sorting
- **Usage**: `isort .` to sort imports

### Linting
- **Package**: `ruff==0.1.3`
- **Purpose**: Fast Python linter
- **Usage**: `ruff check .` to lint code

### Type Checking
- **Package**: `mypy==1.6.1`
- **Purpose**: Static type checking
- **Usage**: `mypy app tests` to check types

## Testing

### PyTest
- **Package**: `pytest==7.4.3`
- **Purpose**: Testing framework
- **Usage**: Running tests
- **Extensions**:
  - `pytest-asyncio==0.21.1`: Async test support
  - `pytest-cov==4.1.0`: Coverage reporting
  - `httpx==0.25.0`: Async HTTP client for testing

## Utility

### Environment Variables
- **Package**: `python-dotenv==1.0.0`
- **Purpose**: Environment variable management
- **Usage**: Loading .env files

### Multipart
- **Package**: `python-multipart==0.0.6`
- **Purpose**: Handling multipart form data
- **Usage**: File uploads

## Version Management

All dependencies are pinned to specific versions for reproducibility. To update:

1. Check for updates:
```bash
pip list --outdated
```

2. Update specific package:
```bash
pip install --upgrade package-name
```

3. Update requirements.txt:
```bash
pip freeze > requirements.txt
```

## Development Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependency Groups

- **Production**: Core dependencies needed for running the application
- **Development**: Tools for development and testing
- **Testing**: Dependencies only needed for running tests

## Compatibility Notes

- Python version: >=3.9
- OS compatibility: Cross-platform (Windows, Linux, MacOS)
- Memory requirements: Minimum 4GB RAM recommended 