from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
from app.services.ai_processor import AIProcessor
from app.config import settings
from app.utils.logging import logger

class DocumentEditor:
    def __init__(self):
        self.ai_processor = AIProcessor()
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.document_states: Dict[str, str] = {}
        self.change_history: Dict[str, List[Dict[str, Any]]] = {}

    async def apply_changes(self, document_id: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Apply changes to document and track history"""
        try:
            if document_id not in self.documents:
                raise ValueError(f"Document {document_id} not found")

            # Format changes with strikeout and highlighting
            formatted_changes = {
                **changes,
                "formatting": {
                    "original": {"strikethrough": True},
                    "new": {"highlight": True}
                },
                "timestamp": datetime.now().isoformat()
            }

            # Apply the changes
            document = self.documents[document_id]
            updated_document = await self._apply_document_changes(document, formatted_changes)
            self.documents[document_id] = updated_document

            # Update change history
            await self.update_appendix(document_id, formatted_changes)

            # Update document state
            self._update_document_state(document_id, "reviewing")

            return {
                "document_id": document_id,
                "original": document,
                "modified": updated_document,
                "changes": formatted_changes,
                "state": self.document_states[document_id],
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error applying changes to document {document_id}: {str(e)}")
            raise

    async def update_appendix(self, document_id: str, changes: Dict[str, Any]) -> None:
        """Update document appendix with change history"""
        try:
            if document_id not in self.change_history:
                self.change_history[document_id] = []

            appendix_entry = {
                "timestamp": datetime.now().isoformat(),
                "changes": changes,
                "user": changes.get("user", "unknown"),
                "type": changes.get("action", "unknown")
            }

            self.change_history[document_id].append(appendix_entry)
            logger.info(f"Updated appendix for document {document_id}")

        except Exception as e:
            logger.error(f"Error updating appendix for document {document_id}: {str(e)}")
            raise

    async def create_document(self, document_id: str, content: str) -> Dict[str, Any]:
        """Create new document"""
        try:
            if document_id in self.documents:
                raise ValueError(f"Document {document_id} already exists")

            document = {
                "content": content,
                "created_at": datetime.now().isoformat(),
                "version": 1
            }

            self.documents[document_id] = document
            self.document_states[document_id] = "draft"
            self.change_history[document_id] = []

            return {
                "document_id": document_id,
                "document": document,
                "state": "draft"
            }

        except Exception as e:
            logger.error(f"Error creating document {document_id}: {str(e)}")
            raise

    async def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document and its current state"""
        try:
            if document_id not in self.documents:
                raise ValueError(f"Document {document_id} not found")

            return {
                "document_id": document_id,
                "document": self.documents[document_id],
                "state": self.document_states[document_id],
                "history": self.change_history.get(document_id, [])
            }

        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {str(e)}")
            raise

    async def finalize_document(self, document_id: str) -> Dict[str, Any]:
        """Finalize document and lock for further changes"""
        try:
            if document_id not in self.documents:
                raise ValueError(f"Document {document_id} not found")

            self._update_document_state(document_id, "final")
            
            return await self.get_document(document_id)

        except Exception as e:
            logger.error(f"Error finalizing document {document_id}: {str(e)}")
            raise

    async def restore_original(self, document_id: str) -> Dict[str, Any]:
        """Restore document to original state"""
        try:
            if document_id not in self.documents:
                raise ValueError(f"Document {document_id} not found")

            # Clear change history
            self.change_history[document_id] = []
            self._update_document_state(document_id, "draft")

            return await self.get_document(document_id)

        except Exception as e:
            logger.error(f"Error restoring document {document_id}: {str(e)}")
            raise

    def _update_document_state(self, document_id: str, state: str) -> None:
        """Update document state"""
        valid_states = ["draft", "reviewing", "final"]
        if state not in valid_states:
            raise ValueError(f"Invalid state: {state}")
        self.document_states[document_id] = state

    async def _apply_document_changes(self, document: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
        """Apply changes to document content"""
        try:
            # Deep copy the document to avoid mutations
            updated_document = document.copy()
            
            # Apply the changes based on the action type
            if changes.get("action") == "edit":
                updated_document["content"] = await self._apply_edit(
                    document["content"],
                    changes.get("text", ""),
                    changes.get("position", 0)
                )
            elif changes.get("action") == "suggestion":
                updated_document["suggestions"] = updated_document.get("suggestions", [])
                updated_document["suggestions"].append(changes)
            
            updated_document["version"] = document.get("version", 0) + 1
            updated_document["last_modified"] = datetime.now().isoformat()
            
            return updated_document

        except Exception as e:
            logger.error(f"Error applying document changes: {str(e)}")
            raise

    async def _apply_edit(self, content: str, new_text: str, position: int) -> str:
        """Apply edit to content at specific position"""
        try:
            return content[:position] + new_text + content[position:]
        except Exception as e:
            logger.error(f"Error applying edit: {str(e)}")
            raise 