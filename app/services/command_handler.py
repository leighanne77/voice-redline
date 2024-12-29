from typing import Dict, Any
from tests.constants.test_messages import MessageType
from tests.constants.message_loader import MessageLoader

class CommandHandler:
    def __init__(self):
        self.message_loader = MessageLoader()
        self.supported_commands = [
            # Basic editing commands
            "delete", "insert", "replace", "undo",
            # Redlining commands
            "start redlining", "stop redlining",
            # Cursor movement commands
            "move cursor up", "move cursor down", "go forward",
            "go forward two", "move cursor to the words",
            # Suggestion commands
            "make suggestion", "accept suggested",
            # Document state commands
            "clear markup, restore original", "accept all, move to final"
        ]
        self.is_redlining = False
        self.current_position = 0

    def process_command(self, command: str) -> Dict[str, Any]:
        """Process text command"""
        if not command:
            return {
                "error": self.message_loader.get_message(MessageType.ERROR_INVALID_COMMAND)
            }

        command_type = command.lower()
        
        if not any(cmd in command_type for cmd in self.supported_commands):
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_INVALID_COMMAND,
                    command=command
                )
            }

        try:
            # Redlining controls
            if "start redlining" in command_type:
                self.is_redlining = True
                return {"message": self.message_loader.get_message(MessageType.COMMAND_START)}
                
            elif "stop redlining" in command_type:
                self.is_redlining = False
                return {"message": self.message_loader.get_message(MessageType.COMMAND_STOP)}

            # Cursor movement
            elif "move cursor up" in command_type:
                return {"message": self.message_loader.get_message(MessageType.COMMAND_MOVE_UP)}
                
            elif "move cursor down" in command_type:
                return {"message": self.message_loader.get_message(MessageType.COMMAND_MOVE_DOWN)}
                
            elif "go forward two" in command_type:
                return {
                    "message": self.message_loader.get_message(
                        MessageType.COMMAND_MOVE_FORWARD,
                        steps=2
                    )
                }
                
            elif "go forward" in command_type:
                return {"message": self.message_loader.get_message(MessageType.COMMAND_MOVE_FORWARD)}
                
            elif "move cursor to the words" in command_type:
                target_text = command_type.split("move cursor to the words")[1].strip()
                return {
                    "message": self.message_loader.get_message(
                        MessageType.COMMAND_MOVE_TO,
                        text=target_text
                    )
                }

            # Suggestion handling
            elif "make suggestion" in command_type:
                return {"message": self.message_loader.get_message(MessageType.COMMAND_SUGGEST)}
                
            elif "accept suggested" in command_type:
                return {"message": self.message_loader.get_message(MessageType.COMMAND_ACCEPT)}

            # Document state
            elif "clear markup, restore original" in command_type:
                return {"message": self.message_loader.get_message(MessageType.COMMAND_CLEAR)}
                
            elif "accept all, move to final" in command_type:
                return {"message": self.message_loader.get_message(MessageType.COMMAND_ACCEPT_ALL)}
            
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    def handle_voice_command(self, audio: bytes) -> Dict[str, Any]:
        """Handle voice command"""
        if not audio:
            return {
                "error": self.message_loader.get_message(MessageType.ERROR_NO_SELECTION)
            }

        try:
            # Process audio to text (placeholder)
            command = "sample command from voice"
            return self.process_command(command)
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    def validate_command(self, command: str) -> Dict[str, Any]:
        """Validate command format"""
        if not command:
            return {
                "error": self.message_loader.get_message(MessageType.ERROR_INVALID_COMMAND)
            }
            
        command_parts = command.split()
        if not any(cmd in command.lower() for cmd in self.supported_commands):
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_INVALID_COMMAND,
                    command=command
                )
            }
            
        return {"valid": True}

    def parse_command_parameters(self, command: str) -> Dict[str, Any]:
        """Parse command parameters"""
        validation_result = self.validate_command(command)
        if "error" in validation_result:
            return validation_result

        try:
            parts = command.split()
            command_type = parts[0]
            parameters = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            return {
                "type": command_type,
                "parameters": parameters,
                "message": self.message_loader.get_message(
                    MessageType.SUCCESS_CHANGE,
                    change_type=command_type
                )
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }