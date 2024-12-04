from typing import Dict, Any, Optional
from app.utils.logging import log_error, log_info

class CommandHandler:
    """Handles processing and validation of voice commands"""
    
    def __init__(self):
        self.cursor_commands = {
            "up": self._move_cursor_up,
            "down": self._move_cursor_down,
            "forward": self._move_cursor_forward,
            "back": self._move_cursor_back,
            "to": self._move_cursor_to
        }
        log_info("Initialized CommandHandler")
    
    async def handle(self, command: str) -> Dict[str, Any]:
        """Process a voice command and return appropriate action"""
        try:
            if not command:
                raise ValueError("Empty command received")
                
            log_info(f"Processing command: {command}")
            
            action = self._determine_action(command)
            result = {
                "action": action,
                "content": self._process_content(command, action),
                "position": self._determine_position(command),
                "confidence": 1.0
            }
            
            log_info(f"Command processed successfully: {result}")
            return result
            
        except Exception as e:
            log_error(f"Error processing command: {str(e)}")
            return {
                "error": str(e),
                "action": None,
                "confidence": 0.0
            }
    
    def _determine_action(self, command: str) -> str:
        """Determine the action type from the command"""
        command = command.lower()
        
        # Redlining controls
        if "start redlining" in command:
            return "start"
        elif "stop redlining" in command:
            return "stop"
            
        # Cursor movement
        elif any(word in command for word in ["move cursor", "go"]):
            return "move"
            
        # Document changes
        elif "make suggestion" in command:
            return "suggest"
        elif "accept suggested" in command:
            return "accept"
        elif "clear markup" in command or "restore original" in command:
            return "restore"
        elif "accept all" in command or "move to final" in command:
            return "accept_all"
            
        # Default actions
        elif "comment" in command:
            return "comment"
        elif "highlight" in command:
            return "highlight"
        else:
            return "unknown"
    
    def _process_content(self, command: str, action: str) -> Optional[str]:
        """Process the content based on action type"""
        if action == "move":
            for direction, func in self.cursor_commands.items():
                if direction in command:
                    return func(command)
        return command
    
    def _determine_position(self, command: str) -> str:
        """Determine the position for the action"""
        if "paragraph" in command:
            return "paragraph"
        elif "selection" in command:
            return "selection"
        return "current"
    
    # Cursor movement helpers
    def _move_cursor_up(self, command: str) -> str:
        return "up"
    
    def _move_cursor_down(self, command: str) -> str:
        return "down"
    
    def _move_cursor_forward(self, command: str) -> str:
        # Check for numbers ("forward two")
        words = command.split()
        try:
            index = words.index("forward")
            if len(words) > index + 1 and words[index + 1].isdigit():
                return f"forward {words[index + 1]}"
        except ValueError:
            pass
        return "forward"
    
    def _move_cursor_back(self, command: str) -> str:
        return "back"
    
    def _move_cursor_to(self, command: str) -> str:
        # Extract target words after "to the words"
        try:
            index = command.index("to the words")
            return command[index + 13:].strip()
        except ValueError:
            return ""