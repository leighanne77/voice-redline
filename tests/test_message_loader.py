import pytest
from constants.test_messages import MessageType
from constants.message_loader import MessageLoader
from constants.test_messages import MessageType

def test_message_loader():
    loader = MessageLoader()
    
    # Update error message tests to use new MessageType
    assert loader.get_message(MessageType.ERROR_INVALID_FORMAT) == "Audio format is invalid or corrupted"
    
    assert loader.get_message(
        MessageType.ERROR_FILE_TOO_LARGE, 
        size=10
    ) == "Audio file exceeds maximum size limit of 10MB"
    
    assert loader.get_message(
        MessageType.ERROR_NOT_FOUND,
        doc_id="123"
    ) == "Document 123 not found"

def test_success_messages():
    loader = MessageLoader()
    
    # Test basic success message
    assert loader.get_success_message("audio", "success_process") == "Audio processed successfully"
    
    # Test success message with parameters
    assert loader.get_success_message(
        "connection", 
        "closed",
        reason="user disconnected"
    ) == "Connection closed: user disconnected"

def test_invalid_messages():
    loader = MessageLoader()
    
    # Test invalid error type
    with pytest.raises(ValueError):
        loader.get_error_message("not_an_enum")
    
    # Test invalid success message category
    with pytest.raises(ValueError):
        loader.get_success_message("invalid_category", "invalid_key") 

def test_message_mapping():
    loader = MessageLoader()
    
    # Test command messages
    assert loader.get_message(MessageType.COMMAND_DELETE) == "Deleting selected text"
    
    # Test with parameters
    assert loader.get_message(
        MessageType.COMMAND_REPLACE,
        new_text="Hello world"
    ) == "Replacing selected text with: Hello world"
    
    # Test error messages
    assert loader.get_message(
        MessageType.ERROR_INVALID_COMMAND,
        command="unknown"
    ) == "Invalid command: unknown"
    
    # Test success messages
    assert loader.get_message(
        MessageType.SUCCESS_CHANGE,
        change_type="deletion"
    ) == "Successfully applied deletion" 