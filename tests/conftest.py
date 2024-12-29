import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import os
from fastapi.testclient import TestClient
from app.main import app
from app.services.ai_processor import AIProcessor
from tests.constants.test_messages import TEST_MESSAGES, MessageType

# Constants
TEST_DATA_DIR = Path(__file__).parent / "data"

@pytest.fixture
def test_messages():
    """Fixture for test messages"""
    return TEST_MESSAGES

@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def mock_groq():
    """Fixture for mocked Groq client"""
    with patch('groq.Client') as mock:
        yield mock

@pytest.fixture
def ai_processor(mock_groq):
    """Fixture for AIProcessor instance"""
    return AIProcessor()

@pytest.fixture
def sample_audio_data():
    """Fixture for sample audio data"""
    audio_file = TEST_DATA_DIR / "sample_audio.wav"
    if not audio_file.exists():
        from tests.data.generate_sample_audio import create_sample_wav
        create_sample_wav()
    return audio_file.read_bytes()

@pytest.fixture
def sample_document():
    """Fixture for sample document data"""
    return {
        "document_id": "test_doc_1",
        "content": "Sample test document content",
        "version": 1
    }
