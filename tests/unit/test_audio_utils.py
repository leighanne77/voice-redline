import pytest
from app.utils.audio import validate_audio_format, get_audio_duration, get_audio_properties
from tests.constants.message_loader import MessageLoader

def test_audio_validation(message_loader):
    invalid_audio = b"invalid data"
    result = validate_audio_format(invalid_audio)
    assert not result, message_loader.get_message(
        "audio.invalid_format",
        lang="en"
    )

def test_file_size(message_loader):
    size_mb = 10
    error_msg = message_loader.get_message(
        "audio.file_too_large",
        lang="es",
        size=size_mb
    )
    assert "10MB" in error_msg

def test_audio_duration(test_messages, sample_audio_data):
    duration = get_audio_duration(sample_audio_data)
    assert duration > 0, test_messages["audio"]["no_audio_data"]
    assert duration < 60, test_messages["audio"]["invalid_duration"].format(seconds=60)
