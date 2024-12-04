import pytest
from app.utils.audio import (
    validate_audio_format,
    convert_audio_format,
    get_audio_duration
)

def test_validate_audio_format():
    """Test audio format validation"""
    valid_data = b"RIFF....WAVEfmt " # Mock WAV header
    assert validate_audio_format(valid_data) is True
    
    invalid_data = b"invalid audio data"
    assert validate_audio_format(invalid_data) is False

def test_convert_audio_format():
    """Test audio format conversion"""
    test_audio = b"test audio data"
    result = convert_audio_format(test_audio, "wav")
    assert isinstance(result, bytes)

def test_get_audio_duration():
    """Test audio duration calculation"""
    try:
        with open("tests/data/sample_audio.wav", "rb") as f:
            duration = get_audio_duration(f.read())
            assert isinstance(duration, float)
            assert duration > 0
    except FileNotFoundError:
        # Generate sample file if it doesn't exist
        from tests.data.generate_sample_audio import create_sample_wav
        create_sample_wav()
        # Retry test
        with open("tests/data/sample_audio.wav", "rb") as f:
            duration = get_audio_duration(f.read())
            assert isinstance(duration, float)
            assert duration > 0
