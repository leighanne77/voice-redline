import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

def test_complete_workflow(client, sample_audio_path, auth_headers):
    """
    Test complete user workflow from voice command to document update
    """
    # Step 1: Health check
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    # Step 2: Upload voice command
    with open(sample_audio_path, "rb") as audio_file:
        files = {"file": ("test.wav", audio_file, "audio/wav")}
        response = client.post(
            "/voice/upload",
            files=files,
            headers=auth_headers
        )
        assert response.status_code == 200
        result = response.json()
        assert "action" in result

    # Step 3: Verify processing status
    command_id = result.get("id")
    if command_id:
        for _ in range(5):  # Poll for up to 5 seconds
            response = client.get(f"/status/{command_id}")
            if response.json().get("status") == "completed":
                break
            time.sleep(1)
        
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    # Step 4: Verify results
    assert result.get("confidence", 0) > 0.8
    assert "content" in result 