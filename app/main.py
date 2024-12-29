import logging
from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

from app.services.ai_processor import AIProcessor
from app.services.document_editor import DocumentEditor
from app.middleware.rate_limit import RateLimiter
from tests.constants.test_messages import MessageType
from tests.constants.message_loader import MessageLoader
from app.config import settings

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Redline", version="1.0.0")

# Initialize services
ai_processor = AIProcessor()
document_editor = DocumentEditor()
rate_limiter = RateLimiter()
message_loader = MessageLoader()

# Add rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    await rate_limiter.check_rate_limit(request)
    response = await call_next(request)
    return response

# Configure CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager with enhanced error handling
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.document_sessions: Dict[str, List[WebSocket]] = {}
        self.user_cursors: Dict[str, Dict[str, int]] = {}  # track cursor positions

    async def connect(self, websocket: WebSocket, document_id: str, user_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        if document_id not in self.document_sessions:
            self.document_sessions[document_id] = []
        self.document_sessions[document_id].append(websocket)
        self.user_cursors[user_id] = {"document_id": document_id, "position": 0}
        
        # Broadcast user joined message
        await self.broadcast_to_document(
            document_id,
            {"type": "user_joined", "user_id": user_id}
        )

    def disconnect(self, websocket: WebSocket, document_id: Optional[str] = None):
        self.active_connections.remove(websocket)
        if document_id and document_id in self.document_sessions:
            self.document_sessions[document_id].remove(websocket)
        logger.info(f"WebSocket connection closed for document: {document_id}")

    async def broadcast_to_document(self, document_id: str, message: Dict[str, Any]):
        """Broadcast to all clients viewing the same document"""
        if document_id in self.document_sessions:
            for connection in self.document_sessions[document_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Document broadcast error: {str(e)}")

manager = ConnectionManager()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Handle file uploads for processing"""
    try:
        contents = await file.read()
        result = await ai_processor.process_input(contents, "file")
        logger.info(f"File processed successfully: {file.filename}")
        return result
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{document_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    document_id: str,
    user_id: str
):
    """Handle WebSocket connections for real-time collaboration"""
    try:
        await manager.connect(websocket, document_id, user_id)
        await rate_limiter.check_websocket_limit(user_id)
        
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            if data["type"] == "voice_command":
                await rate_limiter.check_voice_limit(websocket)
                result = await ai_processor.process_command(data["command"])
            elif data["type"] == "cursor_move":
                result = await document_editor.update_cursor(
                    document_id,
                    user_id,
                    data["position"]
                )
            elif data["type"] == "suggestion":
                await rate_limiter.check_groq_limit(websocket)
                result = await ai_processor.process_suggestion(
                    document_id,
                    data["text"],
                    data["paragraph_id"]
                )
            
            # Broadcast updates to all users
            await manager.broadcast_to_document(document_id, result)
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.send_json({
            "error": message_loader.get_message(
                MessageType.ERROR_PROCESSING,
                error=str(e)
            )
        })
    finally:
        manager.disconnect(websocket, document_id)

@app.post("/process-command/{document_id}")
async def process_command(document_id: str, command: Dict[str, Any]) -> Dict[str, Any]:
    """Process manual commands"""
    try:
        result = await ai_processor.handle_command(command.get("text", ""))
        logger.info(f"Command processed for document: {document_id}")
        return result
    except Exception as e:
        logger.error(f"Command processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/apply-changes/{document_id}")
async def apply_changes(document_id: str, changes: Dict[str, Any]) -> Dict[str, Any]:
    """Apply document changes"""
    try:
        result = await document_editor.apply_changes(document_id, changes)
        
        await manager.broadcast_to_document(document_id, {
            "type": "document_update",
            "changes": result
        })
        
        logger.info(f"Changes applied and broadcasted for document: {document_id}")
        return result
    except Exception as e:
        logger.error(f"Change application error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{document_id}")
async def get_status(document_id: str) -> Dict[str, Any]:
    """Get system status for specific document"""
    try:
        return {
            "document_id": document_id,
            "is_listening": ai_processor.is_listening,
            "active_connections": len(manager.document_sessions.get(document_id, [])),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
