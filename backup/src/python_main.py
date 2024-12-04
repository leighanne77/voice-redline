from services.audio_service import AudioService
from services.groq_service import GroqService
from services.document_editor import DocumentEditor
import time

class VoiceRedlineApp:
    def __init__(self):
        self.audio_service = AudioService()
        self.groq_service = GroqService()
        self.document_editor = DocumentEditor()

    def process_audio(self, audio_data: bytes):
        transcription = self.groq_service.transcribe_audio(audio_data)
        if transcription:
            processed_text = self.groq_service.process_transcription(transcription)
            changes = self.document_editor.update_document(processed_text)
            redlined = self.document_editor.apply_redline(self.document_editor.get_document(), changes)
            print("Updated document:")
            print(redlined)

    def run(self):
        print("Starting Voice Redline App...")
        self.audio_service.start_continuous_recording(self.process_audio)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping Voice Redline App...")
            self.audio_service.stop_recording()

if __name__ == "__main__":
    app = VoiceRedlineApp()
    app.run()