"""Voice Redline Test Data"""
try:
    from pathlib import Path

    SAMPLE_AUDIO_PATH = Path(__file__).parent / "sample_audio.wav"

    __all__ = ['SAMPLE_AUDIO_PATH']
except ImportError as e:
    print(f"Warning: Some imports failed in tests/data/__init__.py: {str(e)}")
    SAMPLE_AUDIO_PATH = None
