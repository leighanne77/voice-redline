import pytest
from app.config import get_settings

@pytest.fixture
def settings():
    """Fixture for application settings"""
    return get_settings()

# Example test using settings
def test_settings_loading(settings):
    assert settings.GROQ_API_KEY == "test_groq_key"
    assert settings.SECRET_KEY == "test_secret_key"