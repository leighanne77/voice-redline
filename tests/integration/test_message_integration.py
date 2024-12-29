from tests.constants.test_messages import MessageType
from app.services.ai_processor import AIProcessor
from app.services.document_editor import DocumentEditor

def test_complete_message_flow():
    processor = AIProcessor()
    editor = DocumentEditor()
    
    # Test command processing
    command_result = processor.process_command("delete")
    assert command_result["message"] == "Deleting selected text"
    
    # Test document changes
    edit_result = editor.apply_changes("deletion")
    assert edit_result["message"] == "Successfully applied deletion"
    
    # Test error scenarios
    error_result = processor.process_command("invalid")
    assert error_result["error"] == "Invalid command: invalid" 