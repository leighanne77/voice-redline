import pytest
from unittest.mock import Mock, patch
from app.services.command_handler import CommandHandler
from app.config import get_settings

@pytest.fixture
def command_handler():
    return CommandHandler()

@pytest.fixture
def settings():
    """Fixture for application settings"""
    return get_settings()

@pytest.mark.asyncio
async def test_handle_command(command_handler):
    """Test command handling"""
    command = "add comment saying needs revision"
    
    result = await command_handler.handle(command)
    assert isinstance(result, dict)
    assert "action" in result
    assert "content" in result

@pytest.mark.asyncio
async def test_invalid_command(command_handler):
    """Test handling of invalid commands"""
    command = ""
    
    result = await command_handler.handle(command)
    assert isinstance(result, dict)
    assert "error" in result
