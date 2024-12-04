"""Configuration for E2E tests"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import get_test_settings

@pytest.fixture(scope="session")
def test_settings():
    """Provide test settings for the entire test session"""
    return get_test_settings()

@pytest.fixture(scope="session")
def client():
    """Provide a TestClient instance for the entire test session"""
    return TestClient(app)

@pytest.fixture(scope="session")
def base_url():
    """Base URL for E2E tests"""
    return "http://localhost:8000"

@pytest.fixture
def sample_audio_path():
    """Path to sample audio file for testing"""
    return "tests/data/sample_audio.wav"

@pytest.fixture
def auth_headers(test_settings):
    """Authentication headers for API requests"""
    return {
        "Authorization": f"Bearer {test_settings.TEST_API_KEY}"
    } 