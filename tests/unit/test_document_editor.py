import pytest
from app.services.document_editor import DocumentEditor
from tests.constants.test_messages import MessageType

@pytest.fixture
def document_editor():
    return DocumentEditor()

def test_document_creation(test_messages, document_editor):
    doc_id = "test_doc"
    content = "Test content"
    result = document_editor.create_document(doc_id, content)
    assert result["document_id"] == doc_id, test_messages["document"]["creation_failed"]

def test_apply_changes(test_messages, document_editor):
    doc_id = "test_doc"
    changes = {
        "action": "edit",
        "text": "Updated content",
        "position": 0
    }
    result = document_editor.apply_changes(doc_id, changes)
    assert result["status"] == "success", test_messages["document"]["update_failed"]

def test_document_state(test_messages, document_editor):
    doc_id = "test_doc"
    document_editor.create_document(doc_id, "content")
    state = document_editor.document_states.get(doc_id)
    assert state == "draft", test_messages["document"]["invalid_state"]

def test_version_control(test_messages, document_editor):
    doc_id = "test_doc"
    document_editor.create_document(doc_id, "content")
    initial_version = document_editor.documents[doc_id]["version"]
    changes = {"action": "edit", "text": "new", "position": 0}
    document_editor.apply_changes(doc_id, changes)
    new_version = document_editor.documents[doc_id]["version"]
    assert new_version > initial_version, test_messages["document"]["version_conflict"]

def test_document_changes():
    editor = DocumentEditor()
    
    # Test successful change
    result = editor.apply_changes("deletion")
    assert result["message"] == "Successfully applied deletion"
    
    # Test undo
    result = editor.undo_change()
    assert result["message"] == "Successfully undid last change" 