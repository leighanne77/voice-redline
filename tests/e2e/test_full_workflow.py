from tests.constants.test_messages import MessageType

async def test_document_workflow():
    # Test complete workflow with commands
    result = await process_workflow_command("delete")
    assert result["message"] == "Deleting selected text"
    
    result = await process_workflow_command("undo")
    assert result["message"] == "Successfully undid last change" 