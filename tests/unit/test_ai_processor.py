import pytest
from typing import Dict, Any
from datetime import datetime
from app.services.ai_processor import AIProcessor
from app.config import settings
from app.utils.logging import logger

class TestAIProcessor:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.processor = AIProcessor()

    @pytest.fixture
    def sample_document(self) -> str:
        return "This is a sample document for testing purposes."

    @pytest.fixture
    def sample_changes(self) -> Dict[str, Any]:
        return {
            "text": "This is an updated document for testing.",
            "position": 0,
            "formatting": {
                "original": {"strikethrough": True},
                "new": {"highlight": True}
            }
        }

    @pytest.mark.asyncio
    async def test_process_command(self):
        """Test command processing"""
        command = "make suggestion"
        result = await self.processor.process_command(command)
        
        assert isinstance(result, dict)
        assert "action" in result
        assert result["action"] in ["edit", "suggestion", "comment"]

    @pytest.mark.asyncio
    async def test_generate_suggestions(self):
        """Test suggestion generation"""
        text = "This is a test document"
        result = await self.processor.process_command("make suggestion")
        assert isinstance(result, dict)
        assert "action" in result
        assert result["action"] == "suggestion"

    @pytest.mark.asyncio
    async def test_apply_changes(self):
        """Test applying changes to document"""
        changes = {
            "text": "Updated text",
            "position": 0,
            "action": "edit"
        }
        result = await self.processor.handle_command("apply changes")
        assert isinstance(result, dict)
        assert "action" in result

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in processor"""
        result = await self.processor.process_command("")
        assert isinstance(result, dict)
        assert "error" in result or "action" in result

    @pytest.mark.asyncio
    async def test_confidence_scores(self):
        """Test confidence scores in results"""
        result = await self.processor.process_command("make suggestion")
        assert isinstance(result, dict)
        assert "confidence" in result
        assert 0 <= result["confidence"] <= 1

    @pytest.mark.asyncio
    async def test_handle_formatting(self, sample_changes):
        """Test document formatting"""
        result = await self.processor.handle_formatting(sample_changes)
        assert result is not None
        assert "formatting" in result
        assert "original" in result["formatting"]
        assert "new" in result["formatting"]
        assert result["formatting"]["original"]["strikethrough"]
        assert result["formatting"]["new"]["highlight"]

    @pytest.mark.asyncio
    async def test_multiple_suggestions(self, sample_document):
        """Test handling multiple suggestions"""
        result = await self.processor.generate_suggestions(sample_document)
        suggestions = result.get("suggestions", [])
        assert len(suggestions) <= settings.MAX_SUGGESTIONS
        assert len(set(s["text"] for s in suggestions)) == len(suggestions)

    @pytest.mark.asyncio
    async def test_document_state(self, sample_document, sample_changes):
        """Test document state tracking"""
        result = await self.processor.apply_changes(sample_document, sample_changes)
        assert "state" in result
        assert "version" in result
        assert result["state"] in ["draft", "reviewing", "final"]

    @pytest.mark.parametrize("command,expected_action", [
        ("start redlining", "start"),
        ("stop redlining", "stop"),
        ("make suggestion", "suggestion"),
        ("Accept Suggested", "accept"),
        ("Clear markup, restore original", "clear"),
        ("Accept All, Move to Final", "accept_all")
    ])
    @pytest.mark.asyncio
    async def test_command_actions(self, command, expected_action):
        """Test specific command actions"""
        result = await self.processor.process_command(command)
        assert result["action"] == expected_action

    @pytest.mark.asyncio
    async def test_groq_integration(self, sample_document):
        """Test Groq API integration"""
        result = await self.processor.process_with_groq(sample_document)
        assert result is not None
        assert "suggestions" in result
        suggestions = result["suggestions"]
        assert len(suggestions) > 0
        assert all("text" in s for s in suggestions)

    # New settings validation tests
    def test_settings_validation(self):
        """Test settings configuration"""
        assert hasattr(settings, 'MAX_SUGGESTIONS')
        assert isinstance(settings.MAX_SUGGESTIONS, int)
        assert settings.MAX_SUGGESTIONS > 0
        assert hasattr(settings, 'GROQ_API_KEY')
        assert hasattr(settings, 'HOST')
        assert hasattr(settings, 'PORT')
        assert hasattr(settings, 'LOG_LEVEL')

    @pytest.mark.parametrize("setting_name,expected_type", [
        ("MAX_SUGGESTIONS", int),
        ("GROQ_API_KEY", str),
        ("HOST", str),
        ("PORT", int),
        ("LOG_LEVEL", str)
    ])
    def test_settings_types(self, setting_name, expected_type):
        """Test settings types"""
        assert isinstance(getattr(settings, setting_name), expected_type)

    @pytest.mark.asyncio
    async def test_document_state(self):
        """Test document state management"""
        doc_id = "test_doc"
        self.processor.start_listening(doc_id)
        assert self.processor.is_listening is True
        
        self.processor.stop_listening()
        assert self.processor.is_listening is False

    def test_groq_integration(self, test_messages, mock_groq, ai_processor):
        mock_groq.return_value.success = True
        result = ai_processor.process_with_groq("test text")
        assert result["status"] == "success", test_messages["groq"]["api_error"].format(
            error="Processing failed"
        )

    def test_command_processing(self, test_messages, ai_processor):
        result = ai_processor.process_command("test command")
        assert result, test_messages["api"]["invalid_request"].format(
            detail="Invalid command format"
        )
