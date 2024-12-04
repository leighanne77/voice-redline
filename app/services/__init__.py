"""Voice Redline Services Package"""
try:
    from app.services.ai_processor import AIProcessor
    from app.services.document_editor import DocumentEditor

    __all__ = [
        'AIProcessor',
        'DocumentEditor'
    ]
except ImportError as e:
    print(f"Warning: Some imports failed in services/__init__.py: {str(e)}")
    AIProcessor = None
    DocumentEditor = None