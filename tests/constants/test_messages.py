from enum import Enum
from typing import Dict, Any

class MessageType(Enum):
    # Commands and their responses
    COMMAND_DELETE = "delete_text"
    COMMAND_INSERT = "insert_text"
    COMMAND_REPLACE = "replace_text"
    COMMAND_UNDO = "undo_change"
    
    # Error messages
    ERROR_INVALID_COMMAND = "invalid_command"
    ERROR_NO_SELECTION = "no_selection"
    ERROR_PROCESSING = "processing_error"
    
    # Success messages
    SUCCESS_CHANGE = "change_applied"
    SUCCESS_UNDO = "change_undone"

# Mapping of message types to their output strings
MESSAGE_OUTPUTS: Dict[MessageType, str] = {
    MessageType.COMMAND_DELETE: "Deleting selected text",
    MessageType.COMMAND_INSERT: "Inserting text at cursor position",
    MessageType.COMMAND_REPLACE: "Replacing selected text with: {new_text}",
    MessageType.COMMAND_UNDO: "Undoing last change",
    
    MessageType.ERROR_INVALID_COMMAND: "Invalid command: {command}",
    MessageType.ERROR_NO_SELECTION: "No text selected",
    MessageType.ERROR_PROCESSING: "Error processing command: {error}",
    
    MessageType.SUCCESS_CHANGE: "Successfully applied {change_type}",
    MessageType.SUCCESS_UNDO: "Successfully undid last change"
}

def get_message(message_type: MessageType, **kwargs) -> str:
    """Get formatted message for given message type"""
    message_template = MESSAGE_OUTPUTS[message_type]
    try:
        return message_template.format(**kwargs)
    except KeyError:
        return message_template 