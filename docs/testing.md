# Testing Guide

## Message Dictionary

The test message dictionary (`tests/constants/test_messages.py`) contains all test-related messages organized by category:

- Audio Processing
- Document Operations
- WebSocket/Connection
- Authentication
- API Responses
- Groq API

### Usage

```python
def test_example(test_messages):
    assert condition, test_messages["category"]["message_key"].format(
        param="value"
    )
```

## Test Categories

1. Unit Tests (`tests/unit/`)
   - Audio processing
   - AI processing
   - Document operations

2. Integration Tests (`tests/integration/`)
   - API endpoints
   - WebSocket connections
   - Document sessions

3. End-to-End Tests (`tests/e2e/`)
   - Full workflows
   - Extension functionality 