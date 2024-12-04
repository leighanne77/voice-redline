import pytest
from fastapi.testclient import TestClient
from app.config import get_test_settings
from app.main import app
from app.services.ai_processor import AIProcessor

settings = get_test_settings()
client = TestClient(app)

@pytest.fixture
def ai_processor():
    return AIProcessor()

@pytest.mark.asyncio
async def test_ai_integration(ai_processor):
    """Test AI integration with basic commands"""
    text = "This is a test document"
    result = await ai_processor.process_command("make suggestion")
    assert result is not None
    assert "action" in result
    assert result["action"] == "suggestion"

@pytest.mark.asyncio
async def test_ai_error_handling(ai_processor):
    """Test AI error handling"""
    try:
        result = await ai_processor.process_command("")
        assert "error" in result
    except Exception as e:
        assert str(e) != ""

@pytest.mark.asyncio
async def test_ai_command_variations(ai_processor):
    """Test different command variations"""
    commands = [
        ("make suggestion", "suggestion"),
        ("start redlining", "start"),
        ("stop redlining", "stop")
    ]
    
    for command, expected_action in commands:
        result = await ai_processor.process_command(command)
