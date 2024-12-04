import pytest
from fastapi.testclient import TestClient
from app.config import get_test_settings
from app.main import app
from app.services.ai_processor import AIProcessor
from unittest.mock import patch, MagicMock
from groq import Groq
from fastapi import HTTPException

settings = get_test_settings()
client = TestClient(app)

@pytest.fixture
def ai_processor():
    return AIProcessor()

@pytest.mark.asyncio
async def test_groq_connection(ai_processor):
    """Test Groq API connection"""
    result = await ai_processor.process_with_groq("Test connection")
    assert result is not None
    assert "action" in result
    assert result["action"] == "process"

@pytest.mark.asyncio
async def test_groq_command_processing(ai_processor):
    """Test Groq command processing"""
    command = "make suggestion"
    result = await ai_processor.process_with_groq(command)
    assert result is not None
    assert "suggestions" in result
    assert len(result["suggestions"]) > 0

@pytest.mark.asyncio
async def test_groq_error_handling(client):
    """Test Groq error handling"""
    
    # Create a mock AIProcessor that raises exceptions
    mock_processor = MagicMock(spec=AIProcessor)
    
    # Setup different error scenarios
    async def mock_handle_command(text: str):
        if "auth_fail" in text:
            raise Exception("Authentication failed")
        elif "rate_limit" in text:
            raise Exception("Rate limit exceeded")
        elif "timeout" in text:
            raise TimeoutError("Request timed out")
        elif "invalid" in text:
            raise ValueError("Invalid command format")
        raise Exception("Unknown error")

    mock_processor.handle_command.side_effect = mock_handle_command

    # Patch the global ai_processor instance
    with patch('app.main.ai_processor', mock_processor):
        # Test authentication error
        response = client.post(
            "/process-command/test_doc",
            json={"text": "auth_fail test"}
        )
        assert response.status_code == 500
        assert "Authentication failed" in str(response.json())
        
        # Test rate limit error
        response = client.post(
            "/process-command/test_doc",
            json={"text": "rate_limit test"}
        )
        assert response.status_code == 500
        assert "Rate limit exceeded" in str(response.json())
        
        # Test timeout error
        response = client.post(
            "/process-command/test_doc",
            json={"text": "timeout test"}
        )
        assert response.status_code == 500
        assert "timed out" in str(response.json())
        
        # Test validation error
        response = client.post(
            "/process-command/test_doc",
            json={"text": "invalid test"}
        )
        assert response.status_code == 500
        assert "Invalid command" in str(response.json())

        # Test generic error
        response = client.post(
            "/process-command/test_doc",
            json={"text": "generic error"}
        )
        assert response.status_code == 500
        assert "Unknown error" in str(response.json())

@pytest.mark.asyncio
async def test_groq_response_format(ai_processor):
    """Test Groq response format"""
    result = await ai_processor.process_with_groq("Test format")
    assert result is not None
    assert "suggestions" in result
    assert all(isinstance(s, dict) for s in result["suggestions"])
    assert all("text" in s for s in result["suggestions"])
