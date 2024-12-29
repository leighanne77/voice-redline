from tests.constants.test_messages import MessageType

async def test_websocket_commands(websocket):
    await websocket.send_json({
        "type": "command",
        "command": "delete"
    })
    
    response = await websocket.receive_json()
    assert response["message"] == "Deleting selected text" 