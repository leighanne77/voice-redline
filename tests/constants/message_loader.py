from .test_messages import MessageType, get_message

class MessageLoader:
    def __init__(self, default_lang: str = "en"):
        self.default_lang = default_lang
        self.translations = {}
        self.load_translations()

    def get_message(self, message_type: MessageType, **kwargs) -> str:
        """Get message using MessageType enum"""
        if not isinstance(message_type, MessageType):
            raise ValueError("Message type must be a MessageType enum")
        
        return get_message(message_type, **kwargs) 