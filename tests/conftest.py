import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import os

# Mock groq before other imports
groq_mock = MagicMock()
patch('groq.Client', return_value=groq_mock).start()

from fastapi.testclient import TestClient
from app.main import app
from app.services.ai_processor import AIProcessor

# Constants
TEST_DATA_DIR = Path(__file__).parent / "data"

os.environ["TESTING"] = "true"

@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def groq_client():
    """Fixture for mocked Groq client"""
    return groq_mock

@pytest.fixture
def ai_processor():
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
