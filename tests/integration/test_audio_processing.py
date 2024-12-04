import pytest
from pathlib import Path
import asyncio
from typing import Dict, Any
from app.services.ai_processor import AIProcessor
from app.config import settings

class TestAudioProcessing:
    @pytest.fixture
    def processor(self):
        return AIProcessor()

    @pytest.fixture
    def sample_audio_path(self) -> Path:
        return Path("tests/data/sample_audio.wav")

    @pytest.fixture
    async def sample_audio_data(self, sample_audio_path) -> bytes:
        with open(sample_audio_path, "rb") as f:
            return f.read()

    async def test_audio_processing(self, processor, sample_audio_data):
        """Test complete audio processing flow"""
        processor.start_listening("test_doc_1")
        result = await processor.process_input(sample_audio_data, "voice")
        assert result is not None
        assert "status" in result

    async def test_command_recognition(self, processor, sample_audio_data):
        """Test voice command recognition"""
        processor.start_listening("test_doc_1")
        result = await processor.process_input(sample_audio_data, "voice")
        assert "action" in result
        assert result["status"] in ["success", "error"]

    async def test_audio_validation(self, processor, sample_audio_data):
        """Test audio format validation"""
        processor.start_listening("test_doc_1")
        result = await processor.process_input(sample_audio_data, "voice")
        assert result["status"] != "invalid_format"

    async def test_processing_states(self, processor):
        """Test processor state management"""
        assert not processor.is_listening
        processor.start_listening("test_doc_1")
        assert processor.is_listening
        processor.stop_listening()
        assert not processor.is_listening

    async def test_error_handling(self, processor):
        """Test error handling for invalid input"""
        processor.start_listening("test_doc_1")
        with pytest.raises(Exception):
            await processor.process_input(b"invalid_audio_data", "voice")

    @pytest.mark.parametrize("command", [
        "start redlining",
        "stop redlining",
        "move cursor up",
        "make suggestion"
    ])
    async def test_voice_commands(self, processor, command):
        """Test various voice commands"""
        processor.start_listening("test_doc_1")
        result = await processor.handle_command(command)
        assert result is not None
        assert "action" in result
        assert "status" in result

    async def test_concurrent_processing(self, processor, sample_audio_data):
        """Test concurrent audio processing"""
        processor.start_listening("test_doc_1")
        tasks = [
            processor.process_input(sample_audio_data, "voice")
            for _ in range(3)
        ]
        results = await asyncio.gather(*tasks)
        assert all(r is not None for r in results)

    async def test_processing_callback(self, processor):
        """Test command callback functionality"""
        callback_called = False
        
        async def test_callback(result: Dict[str, Any]):
            nonlocal callback_called
            callback_called = True
            
        processor.set_command_callback(test_callback)
        processor.start_listening("test_doc_1")
        await processor.handle_command("test command")
        assert callback_called

    async def test_audio_properties(self, processor, sample_audio_data):
        """Test audio properties validation"""
        processor.start_listening("test_doc_1")
        result = await processor.process_input(sample_audio_data, "voice")
        assert result is not None
        # Add specific audio property checks based on your requirements

    async def test_processing_timeout(self, processor, sample_audio_data):
        """Test processing timeout handling"""
        processor.start_listening("test_doc_1")
        with pytest.raises(asyncio.TimeoutError):
            async with asyncio.timeout(0.1):  # Very short timeout
                await processor.process_input(sample_audio_data * 1000, "voice")  # Large data