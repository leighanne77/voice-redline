import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'python')))

from services.groq_service import GroqService
from services.document_editor import DocumentEditor
from main import VoiceRedlineApp

# Mock the AudioService
class MockAudioService:
    def start_continuous_recording(self, callback):
        callback(b'fake audio data')

    def stop_recording(self):
        pass

class TestVoiceRedlineIntegration(unittest.TestCase):
    def setUp(self):
        self.app = VoiceRedlineApp()
        self.app.audio_service = MockAudioService()
        
    def test_audio_to_document_flow(self):
        # Mock transcription result
        mock_transcription = "This is a test transcription."
        
        # Mock processed text
        mock_processed_text = "This is a processed test transcription."
        
        # Patch the necessary methods
        with patch.object(self.app.groq_service, 'transcribe_audio', return_value=mock_transcription), \
             patch.object(self.app.groq_service, 'process_transcription', return_value=mock_processed_text):
            
            # Call the method we're testing
            self.app.process_audio(b'fake audio data')
            
            # Assert that the document was updated correctly
            self.assertEqual(self.app.document_editor.get_document(), mock_processed_text)
    
    def test_redline_functionality(self):
        original_text = "This is the original text."
        new_text = "This is the updated text."
        
        changes = self.app.document_editor.update_document(new_text)
        redlined = self.app.document_editor.apply_redline(original_text, changes)
        
        # Check if redlined text contains both deletion and addition markers
        self.assertIn("\033[31m", redlined)  # Red for deletions
        self.assertIn("\033[32m", redlined)  # Green for additions

if __name__ == '__main__':
    unittest.main()