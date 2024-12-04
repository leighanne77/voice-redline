"""Voice Redline Utilities Package"""
try:
    from app.utils.audio import validate_audio_format, convert_audio_format, get_audio_duration
    import logging

    __all__ = [
        'validate_audio_format',
        'convert_audio_format',
        'get_audio_duration',
        'logging'
    ]
except ImportError as e:
    print(f"Warning: Some imports failed in utils/__init__.py: {str(e)}")
    validate_audio_format = None
    convert_audio_format = None
    get_audio_duration = None
    logging = None
