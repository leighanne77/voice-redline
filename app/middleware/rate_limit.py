from fastapi import Request, HTTPException
from app.config import settings
import time
from collections import defaultdict
from tests.constants.test_messages import MessageType
from tests.constants.message_loader import MessageLoader
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        self.calls = defaultdict(list)
        self.voice_calls = defaultdict(list)
        self.groq_calls = defaultdict(list)
        self.websocket_calls = defaultdict(list)
        self.message_loader = MessageLoader()
    
    async def check_rate_limit(self, request: Request):
        """Check general API rate limit"""
        client_ip = request.client.host
        now = time.time()
        
        # Clean old calls
        self.calls[client_ip] = [
            call_time for call_time in self.calls[client_ip]
            if now - call_time < settings.API_CALL_INTERVAL
        ]
        
        if len(self.calls[client_ip]) >= settings.API_CALL_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=self.message_loader.get_message(MessageType.ERROR_RATE_LIMIT)
            )
        
        self.calls[client_ip].append(now)

    async def check_voice_limit(self, request: Request):
        """Check voice command rate limit"""
        client_ip = request.client.host
        now = time.time()
        
        # Clean old voice calls
        self.voice_calls[client_ip] = [
            call_time for call_time in self.voice_calls[client_ip]
            if now - call_time < settings.VOICE_CALL_INTERVAL
        ]
        
        if len(self.voice_calls[client_ip]) >= settings.VOICE_CALL_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=self.message_loader.get_message(MessageType.ERROR_VOICE_COOLDOWN)
            )
        
        self.voice_calls[client_ip].append(now)

    async def check_groq_limit(self, request: Request):
        """Check Groq API rate limit"""
        client_ip = request.client.host
        now = time.time()
        
        # Clean old Groq API calls
        self.groq_calls[client_ip] = [
            call_time for call_time in self.groq_calls[client_ip]
            if now - call_time < settings.GROQ_CALL_INTERVAL
        ]
        
        if len(self.groq_calls[client_ip]) >= settings.GROQ_CALL_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=self.message_loader.get_message(MessageType.ERROR_API_LIMIT)
            )
        
        self.groq_calls[client_ip].append(now)

    async def check_websocket_limit(self, client_ip: str):
        """Check WebSocket message rate limit"""
        now = time.time()
        
        # Clean old WebSocket calls
        self.websocket_calls[client_ip] = [
            call_time for call_time in self.websocket_calls[client_ip]
            if now - call_time < settings.WEBSOCKET_MESSAGE_INTERVAL
        ]
        
        if len(self.websocket_calls[client_ip]) >= settings.WEBSOCKET_MESSAGE_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=self.message_loader.get_message(MessageType.ERROR_WEBSOCKET_LIMIT)
            )
        
        self.websocket_calls[client_ip].append(now) 