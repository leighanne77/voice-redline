import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

@pytest.fixture
def mock_extension():
    return MagicMock()

def test_extension_initialization(test_messages, mock_extension):
    assert mock_extension.initialized, test_messages["extension"]["init_failed"]

def test_voice_command_processing(test_messages, client, mock_extension):
    command = "edit paragraph"
    response = client.post(
        "/process-command/test_doc",
        json={"command": command}
    )
    assert response.status_code == 200, test_messages["extension"]["command_failed"]

def test_document_markup(test_messages, mock_extension):
    changes = {"text": "new text", "position": 0}
    result = mock_extension.apply_markup(changes)
    assert result["success"], test_messages["extension"]["markup_failed"]

def test_websocket_integration(test_messages, client):
    with client.websocket_connect("/ws/test_doc") as websocket:
        data = websocket.receive_json()
        assert data["connected"], test_messages["extension"]["connection_failed"] 