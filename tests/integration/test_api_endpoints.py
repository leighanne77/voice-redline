import pytest
from fastapi.testclient import TestClient
from tests.constants.test_messages import MessageType

def test_health_check(test_messages, client):
    response = client.get("/")
    assert response.status_code == 200, test_messages["api"]["server_error"]

def test_document_upload(test_messages, client, sample_document):
    response = client.post("/upload", json=sample_document)
    assert response.status_code == 200, test_messages["document"]["update_failed"].format(
        error="Upload failed"
    )

def test_rate_limiting(test_messages, client):
    # Make multiple requests to trigger rate limit
    for _ in range(100):
        response = client.get("/")
    assert response.status_code == 429, test_messages["api"]["rate_limit"].format(
        seconds=60
    ) 

def test_groq_connection(test_messages, client):
    """Test Groq API connection through the application endpoint"""
    test_text = "Test message"
    response = client.post("/process-text", json={"text": test_text})
    
    assert response.status_code == 200, test_messages["api"]["server_error"]
    assert "response" in response.json(), "No response from Groq API"
    
    # Check if we got a valid response
    result = response.json()
    assert result["status"] == "success", f"API call failed: {result.get('error', 'Unknown error')}" 

async def test_command_endpoint(client):
    response = await client.post("/process-command/doc1", json={
        "command": "delete"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Deleting selected text"
    
    response = await client.post("/process-command/doc1", json={
        "command": "invalid"
    })
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid command: invalid" 