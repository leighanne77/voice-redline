import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from voice_processor import process_voice, VoiceProcessingError
from config import settings

def test_process_voice():
    # Path to the sample audio file
    audio_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample_audio.wav')

    # Read the audio file
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    try:
        # Process the audio
        result = process_voice(audio_data)

        # Check if the result is a non-empty string
        assert isinstance(result, str)
        assert len(result) > 0

        print(f"Transcription result: {result}")
    except VoiceProcessingError as e:
        pytest.fail(f"Voice processing failed: {str(e)}")

if __name__ == "__main__":
    # Verify that the GROQ_API_KEY is set
    if not settings.GROQ_API_KEY:
        print("Error: GROQ_API_KEY is not set in the .env file.")
        sys.exit(1)

    # Run the test
    test_process_voice()