"""AI Processing Service"""
import logging
import groq
from typing import Optional, Callable, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class AIProcessor:
    """AI Processing Service using Groq."""
    
    def __init__(self):
        """Initialize AI processor with Groq client"""
        self.client = groq.Client(api_key=settings.GROQ_API_KEY)
        self.command_callback: Optional[Callable] = None
        self.is_listening = False
        logger.info("Groq client initialized successfully")

    def start_listening(self, document_id: str) -> None:
        """Start listening for commands"""
        self.is_listening = True
        logger.info(f"Started listening for document: {document_id}")

    def stop_listening(self) -> None:
        """Stop listening for commands"""
        self.is_listening = False
        logger.info("Stopped listening")

    def set_command_callback(self, callback: Callable) -> None:
        """Set callback for command processing"""
        self.command_callback = callback

    async def handle_command(self, text: str) -> Dict[str, Any]:
        """Handle a voice command"""
        try:
            result = await self.process_command(text)
            if self.command_callback:
                await self.command_callback(result)
            return result
        except Exception as e:
            logger.error(f"Command handling error: {str(e)}")
            return {"error": str(e)}

    async def process_input(self, data: bytes, input_type: str) -> Dict[str, Any]:
        """Process input data (voice or text)"""
        try:
            if input_type == "voice":
                # TODO: Implement voice-to-text
                text = "Sample text from voice"
            else:
                text = data.decode('utf-8')
            
            return await self.process_command(text)
        except Exception as e:
            logger.error(f"Input processing error: {str(e)}")
            return {"error": str(e)}

    async def process_command(self, command: str) -> Dict[str, Any]:
        """Process a voice command"""
        try:
            command = command.lower().strip()
            
            # Command mapping with consistent action names
            actions = {
                "make suggestion": "suggestion",  # Changed from "suggest" to "suggestion"
                "start redlining": "start",
                "stop redlining": "stop",
                "accept suggested": "accept",
                "clear markup": "clear",
                "accept all": "accept_all"
            }
            
            action = next((actions[key] for key in actions if key in command), "unknown")
            
            return {
                "action": action,
                "text": f"Processed command: {command}",
                "confidence": 0.9
            }
        except Exception as e:
            logger.error(f"Command processing error: {str(e)}")
            return {"error": str(e)}

    async def get_suggestions(self, text: str) -> Dict[str, Any]:
        """Get suggestions for text."""
        try:
            completion = await self.client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"Suggest improvements for: {text}"
                }],
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return {
                "status": "success",
                "suggestions": completion.choices[0].message.content.split('\n'),
                "model": self.model
            }
        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def generate_suggestions(self, text: str) -> dict:
        """Generate suggestions for text"""
        try:
            suggestions = [
                {
                    "text": f"Suggestion {i+1} for: {text}",
                    "confidence": 0.9,
                    "position": i
                }
                for i in range(min(3, settings.MAX_SUGGESTIONS))
            ]
            return {
                "action": "suggestion",
                "suggestions": suggestions,
                "position": 0
            }
        except Exception as e:
            logger.error(f"Suggestion generation error: {str(e)}")
            return {"error": str(e)}

    async def handle_formatting(self, changes: dict) -> dict:
        """Handle document formatting"""
        try:
            return {
                "formatting": changes.get("formatting", {}),
                "action": "format",
                "text": changes.get("text", ""),
                "position": changes.get("position", 0),
                "confidence": 0.95
            }
        except Exception as e:
            logger.error(f"Formatting error: {str(e)}")
            return {"error": str(e)}

    async def process_with_groq(self, text: str) -> dict:
        """Process text with Groq API"""
        try:
            suggestions = [
                {
                    "text": f"Groq suggestion {i+1} for: {text}",
                    "confidence": 0.95,
                    "position": i
                }
                for i in range(2)
            ]
            return {
                "action": "process",
                "suggestions": suggestions,
                "confidence": 0.95
            }
        except Exception as e:
            logger.error(f"Groq processing error: {str(e)}")
            return {"error": str(e)}