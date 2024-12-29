"""AI Processing Service"""
import logging
import groq
from typing import Optional, Callable, Dict, Any, List
from app.config import settings
from tests.constants.test_messages import MessageType
from tests.constants.message_loader import MessageLoader

logger = logging.getLogger(__name__)

class AIProcessor:
    """AI Processing Service using Groq."""
    
    def __init__(self):
        """Initialize AI processor with Groq client"""
        self.client = groq.Client(api_key=settings.GROQ_API_KEY)
        self.message_loader = MessageLoader()
        self.command_callback: Optional[Callable] = None
        self.is_listening = False
        self.max_size = 10  # MB
        self.conversation_buffer = []
        self.change_history: List[Dict[str, Any]] = []
        self.current_paragraph = ""
        self.original_text = {}  # Store original text for each paragraph
        self.active_users = {}  # Track active users
        self.cursor_positions = {}  # Track cursor positions
        self.highlighting = {}  # Track highlights
        self.preview_suggestions = {}  # Track real-time previews
        logger.info("Groq client initialized successfully")

    async def start_listening(self, document_id: str) -> Dict[str, Any]:
        """Start listening for conversation"""
        self.is_listening = True
        logger.info(f"Started listening for document: {document_id}")
        return {
            "message": self.message_loader.get_message(MessageType.COMMAND_START)
        }

    async def stop_listening(self) -> Dict[str, Any]:
        """Stop listening for conversation"""
        self.is_listening = False
        logger.info("Stopped listening")
        return {
            "message": self.message_loader.get_message(MessageType.COMMAND_STOP)
        }

    async def process_conversation(self, text: str, paragraph_id: str) -> Dict[str, Any]:
        """Process conversation and generate suggestions"""
        if not self.is_listening:
            return {
                "error": self.message_loader.get_message(MessageType.ERROR_NOT_LISTENING)
            }

        try:
            # Store original text if not already stored
            if paragraph_id not in self.original_text:
                self.original_text[paragraph_id] = text

            suggestions = await self._get_groq_suggestions(text)
            
            return {
                "message": self.message_loader.get_message(MessageType.SUCCESS_PROCESS),
                "suggestions": suggestions,
                "original_text": self.original_text[paragraph_id],
                "paragraph_id": paragraph_id
            }
        except Exception as e:
            logger.error(f"Error processing conversation: {str(e)}")
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def apply_suggestion(self, paragraph_id: str, suggestion: str) -> Dict[str, Any]:
        """Apply a suggestion to the text"""
        try:
            original = self.original_text.get(paragraph_id, "")
            
            # Log change in history
            self.change_history.append({
                "paragraph_id": paragraph_id,
                "original": original,
                "suggestion": suggestion,
                "timestamp": "timestamp_here"
            })

            return {
                "message": self.message_loader.get_message(MessageType.SUCCESS_CHANGE),
                "new_text": suggestion,
                "original_text": f"<strike>{original}</strike>",
                "paragraph_id": paragraph_id
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def clear_changes(self, paragraph_id: str) -> Dict[str, Any]:
        """Clear changes and restore original text"""
        try:
            original = self.original_text.get(paragraph_id)
            if not original:
                return {
                    "error": self.message_loader.get_message(MessageType.ERROR_NO_ORIGINAL)
                }

            return {
                "message": self.message_loader.get_message(MessageType.COMMAND_CLEAR),
                "text": original,
                "paragraph_id": paragraph_id
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def accept_all_changes(self) -> Dict[str, Any]:
        """Accept all changes and generate appendix"""
        try:
            appendix = self._generate_change_appendix()
            
            return {
                "message": self.message_loader.get_message(MessageType.COMMAND_ACCEPT_ALL),
                "appendix": appendix,
                "changes": self.change_history
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def _get_groq_suggestions(self, text: str) -> List[Dict[str, Any]]:
        """Get suggestions from Groq API"""
        try:
            completion = await self.client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"Suggest improvements for: {text}"
                }],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=2048
            )
            
            suggestions = completion.choices[0].message.content.split('\n')
            return [{"text": s, "confidence": 0.9} for s in suggestions if s.strip()]
            
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise

    def _generate_change_appendix(self) -> str:
        """Generate appendix of all changes"""
        appendix = ["# Document Change History"]
        
        for change in self.change_history:
            appendix.append(f"\n## Paragraph {change['paragraph_id']}")
            appendix.append(f"Original: {change['original']}")
            appendix.append(f"Changed to: {change['suggestion']}")
            appendix.append(f"Timestamp: {change['timestamp']}")
            
        return "\n".join(appendix)

    async def handle_cursor_movement(self, user_id: str, command: str, 
                                  current_position: int) -> Dict[str, Any]:
        """Handle cursor movement commands"""
        try:
            new_position = current_position
            if command == "move cursor up":
                new_position -= 1
            elif command == "move cursor down":
                new_position += 1
            elif command == "go forward":
                new_position += 1
            elif command == "go forward two":
                new_position += 2
            elif "move cursor to the words" in command:
                target_text = command.split("move cursor to the words")[1].strip()
                # Logic to find position of target text
                pass

            self.cursor_positions[user_id] = new_position
            return {
                "message": self.message_loader.get_message(MessageType.COMMAND_MOVE),
                "position": new_position
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def add_user(self, user_id: str) -> Dict[str, Any]:
        """Add user to collaboration session"""
        self.active_users[user_id] = {
            "timestamp": "current_time",
            "cursor_position": 0,
            "changes": []
        }
        return {
            "message": self.message_loader.get_message(MessageType.USER_JOINED)
        }

    async def update_highlighting(self, paragraph_id: str, 
                                changes: Dict[str, Any]) -> Dict[str, Any]:
        """Update visual highlighting"""
        try:
            self.highlighting[paragraph_id] = {
                "original": f"<strike>{changes['original']}</strike>",
                "new": f"<highlight>{changes['new']}</highlight>",
                "timestamp": "current_time"
            }
            return {
                "message": self.message_loader.get_message(MessageType.HIGHLIGHT_UPDATED),
                "highlighting": self.highlighting[paragraph_id]
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def preview_suggestion(self, paragraph_id: str, 
                               suggestion: str) -> Dict[str, Any]:
        """Generate real-time preview of suggestion"""
        try:
            preview = {
                "original": self.original_text.get(paragraph_id, ""),
                "suggested": suggestion,
                "preview_html": self._generate_preview_html(
                    self.original_text.get(paragraph_id, ""),
                    suggestion
                )
            }
            self.preview_suggestions[paragraph_id] = preview
            return {
                "message": self.message_loader.get_message(MessageType.PREVIEW_READY),
                "preview": preview
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    def _generate_preview_html(self, original: str, suggestion: str) -> str:
        """Generate HTML preview with highlighting"""
        return f"""
        <div class="preview-container">
            <div class="original"><strike>{original}</strike></div>
            <div class="suggestion"><highlight>{suggestion}</highlight></div>
        </div>
        """