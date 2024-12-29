"""Configuration settings for the Voice Redline application."""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings."""
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    MAX_SUGGESTIONS: int = 3
    
    # API Configuration
    GROQ_API_KEY: str = "test_groq_key"
    SECRET_KEY: str = "test_secret_key"
    
    # Model Configuration
    PRIMARY_MODEL: str = "mixtral-8x7b-32768"
    FALLBACK_MODEL: str = "whisper-turbo"
    USE_FALLBACK: bool = True
    
    # API Limits
    API_CALL_LIMIT: int = 100
    API_CALL_INTERVAL: int = 3600  # seconds
    VOICE_CALL_LIMIT: int = 30
    VOICE_CALL_INTERVAL: int = 60  # seconds
    GROQ_CALL_LIMIT: int = 50
    GROQ_CALL_INTERVAL: int = 60  # seconds
    WEBSOCKET_MESSAGE_LIMIT: int = 100
    WEBSOCKET_MESSAGE_INTERVAL: int = 60  # seconds
    
    # Model Parameters
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    
    # Document Settings
    MAX_DOCUMENT_SIZE: int = 10  # MB
    SUPPORTED_DOC_TYPES: list = ["google_docs", "microsoft_office"]
    
    # Retry Configuration
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 1  # seconds

    model_config = ConfigDict(
        env_prefix="APP_",
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )

    def __init__(self, **kwargs):
        # Use test values if in test environment
        if os.getenv("TESTING", "false").lower() == "true":
            kwargs.setdefault("GROQ_API_KEY", "test_groq_key")
            kwargs.setdefault("SECRET_KEY", "test_secret_key")
        super().__init__(**kwargs)

def get_settings():
    """Get application settings"""
    return Settings()

def get_test_settings() -> Settings:
    """Get test settings with mock values"""
    os.environ["TESTING"] = "true"
    os.environ["GROQ_API_KEY"] = "test_groq_key"
    os.environ["SECRET_KEY"] = "test_secret_key"
    return Settings()

settings = get_settings() 