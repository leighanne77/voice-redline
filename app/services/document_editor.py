from typing import Dict, Any, List, Optional
from tests.constants.test_messages import MessageType
from tests.constants.message_loader import MessageLoader
import logging

logger = logging.getLogger(__name__)

class DocumentEditor:
    def __init__(self):
        self.message_loader = MessageLoader()
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.document_states: Dict[str, str] = {}
        self.change_history: Dict[str, List[Dict[str, Any]]] = {}
        self.active_users: Dict[str, Dict[str, Any]] = {}
        self.paragraph_locks: Dict[str, str] = {}  # paragraph_id: user_id
        self.preview_states: Dict[str, Dict[str, Any]] = {}

    async def init_document(self, doc_id: str, doc_type: str) -> Dict[str, Any]:
        """Initialize document tracking"""
        try:
            if doc_type not in ["google_docs", "microsoft_office"]:
                return {
                    "error": self.message_loader.get_message(
                        MessageType.ERROR_INVALID_DOC_TYPE,
                        type=doc_type
                    )
                }
            
            self.documents[doc_id] = {
                "type": doc_type,
                "paragraphs": {},
                "users": [],
                "changes": []
            }
            return {
                "message": self.message_loader.get_message(MessageType.DOC_INITIALIZED)
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def add_user(self, doc_id: str, user_id: str) -> Dict[str, Any]:
        """Add user to document session"""
        if doc_id not in self.documents:
            return {
                "error": self.message_loader.get_message(MessageType.ERROR_DOC_NOT_FOUND)
            }
        
        self.active_users[user_id] = {
            "doc_id": doc_id,
            "cursor_position": None,
            "selected_paragraph": None
        }
        self.documents[doc_id]["users"].append(user_id)
        
        return {
            "message": self.message_loader.get_message(MessageType.USER_JOINED)
        }

    async def apply_changes(self, doc_id: str, paragraph_id: str, 
                          changes: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Apply changes to document"""
        try:
            # Check document exists
            if doc_id not in self.documents:
                return {
                    "error": self.message_loader.get_message(MessageType.ERROR_DOC_NOT_FOUND)
                }

            # Check paragraph lock
            if paragraph_id in self.paragraph_locks and self.paragraph_locks[paragraph_id] != user_id:
                return {
                    "error": self.message_loader.get_message(
                        MessageType.ERROR_PARAGRAPH_LOCKED,
                        user=self.paragraph_locks[paragraph_id]
                    )
                }

            # Store original if first change
            if paragraph_id not in self.documents[doc_id]["paragraphs"]:
                self.documents[doc_id]["paragraphs"][paragraph_id] = {
                    "original": changes["original"],
                    "current": changes["original"],
                    "history": []
                }

            # Apply changes
            self.documents[doc_id]["paragraphs"][paragraph_id]["current"] = changes["new"]
            self.documents[doc_id]["paragraphs"][paragraph_id]["history"].append({
                "user_id": user_id,
                "timestamp": "current_time",
                "change": changes["new"],
                "original": changes["original"]
            })

            return {
                "message": self.message_loader.get_message(MessageType.CHANGES_APPLIED),
                "html": self._generate_paragraph_html(doc_id, paragraph_id)
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def preview_changes(self, doc_id: str, paragraph_id: str, 
                            suggestion: str) -> Dict[str, Any]:
        """Generate preview of changes"""
        try:
            original = self.documents[doc_id]["paragraphs"][paragraph_id]["current"]
            preview_html = f"""
            <div class="preview-panel">
                <div class="original"><strike>{original}</strike></div>
                <div class="suggestion"><highlight>{suggestion}</highlight></div>
            </div>
            """
            
            self.preview_states[paragraph_id] = {
                "original": original,
                "suggestion": suggestion,
                "html": preview_html
            }
            
            return {
                "message": self.message_loader.get_message(MessageType.PREVIEW_READY),
                "preview": self.preview_states[paragraph_id]
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    async def generate_appendix(self, doc_id: str) -> Dict[str, Any]:
        """Generate change history appendix"""
        try:
            appendix = ["# Document Change History\n"]
            doc = self.documents[doc_id]
            
            for para_id, para_data in doc["paragraphs"].items():
                if para_data["history"]:
                    appendix.append(f"\n## Paragraph {para_id}")
                    appendix.append(f"Original: {para_data['original']}")
                    for change in para_data["history"]:
                        appendix.append(
                            f"Changed to: {change['change']} "
                            f"(by user {change['user_id']} at {change['timestamp']})"
                        )
            
            return {
                "message": self.message_loader.get_message(MessageType.APPENDIX_GENERATED),
                "appendix": "\n".join(appendix)
            }
        except Exception as e:
            return {
                "error": self.message_loader.get_message(
                    MessageType.ERROR_PROCESSING,
                    error=str(e)
                )
            }

    def _generate_paragraph_html(self, doc_id: str, paragraph_id: str) -> str:
        """Generate HTML for paragraph with changes"""
        para_data = self.documents[doc_id]["paragraphs"][paragraph_id]
        return f"""
        <div class="paragraph" id="{paragraph_id}">
            <div class="original"><strike>{para_data['original']}</strike></div>
            <div class="current"><highlight>{para_data['current']}</highlight></div>
        </div>
        """ 