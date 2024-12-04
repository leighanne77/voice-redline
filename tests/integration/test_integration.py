import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import asyncio
import logging
from typing import Dict, Any

from app.main import app
from app.services.ai_processor import AIProcessor
from app.services.document_editor import DocumentEditor
from app.config import get_test_settings

settings = get_test_settings()
client = TestClient(app)

@pytest.fixture
def ai_processor():
    return AIProcessor()

@pytest.fixture
def document_editor():
    return DocumentEditor()

@pytest.fixture
def sample_document() -> Dict[str, str]:
    return {
        "content": "This is a test document.",
        "document_id": "test_doc_1"
    }

@pytest.mark.asyncio
async def test_document_creation(client, document_editor, sample_document):
    """Test document creation and initial processing"""
    try:
        # Create document first
        doc = await document_editor.create_document(
            sample_document["document_id"],
            sample_document["content"]
        )
        assert doc is not None
        
        # Create a temporary file for upload
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp:
            temp.write(sample_document["content"])
            temp.flush()
            
            # Upload the file
            with open(temp.name, 'rb') as f:
                files = {'file': ('test.txt', f, 'text/plain')}
                response = client.post("/upload", files=files)
                
        assert response.status_code == 200
        result = response.json()
        assert "action" in result
        assert "confidence" in result
        assert "text" in result
    except Exception as e:
        pytest.fail(f"Document creation test failed: {str(e)}")
    finally:
        # Cleanup
        import os
        if 'temp' in locals():
            os.unlink(temp.name)

@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_voice_command_processing(client, ai_processor):
    """Test voice command processing"""
    try:
        command = {
            "text": "make suggestion",
            "document_id": "test_doc_1"
        }
        
        response = client.post(
            "/process-command/test_doc_1",
            json=command,
            timeout=3.0
        )
        assert response.status_code == 200
        result = response.json()
        assert "action" in result
    except Exception as e:
        pytest.fail(f"Voice command processing test failed: {str(e)}")