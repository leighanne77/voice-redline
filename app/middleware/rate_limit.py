from fastapi import Request, HTTPException
from app.config import settings
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        self.calls = defaultdict(list)
    
    async def check_rate_limit(self, request: Request):
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
                detail="Rate limit exceeded"
            )
        
        self.calls[client_ip].append(now) 