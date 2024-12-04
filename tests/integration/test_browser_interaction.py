import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from app.config import get_test_settings
from app.main import app

settings = get_test_settings()
client = TestClient(app)

def test_browser_health_check():
    """Test browser health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_browser_docs_access():
    """Test access to API documentation"""
    response = client.get("/docs")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_browser_file_upload():
    """Test file upload functionality"""
    file_path = Path("tests/data/sample.txt")
    if not file_path.exists():
        file_path.write_text("Test content")
    
    with open(file_path, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )
    assert response.status_code in [200, 201]

@pytest.mark.asyncio
async def test_browser_command_processing():
    """Test command processing through browser"""
    command = {"text": "make suggestion"}
    response = client.post("/process-command/test_doc_1", json=command)
    assert response.status_code == 200
    assert "action" in response.json()

def test_browser_error_handling():
    """Test browser error handling"""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404
