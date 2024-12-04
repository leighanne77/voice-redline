import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from dotenv import load_dotenv
from voice_processor import process_voice, detect_voice_commands
from ai_processor import generate_suggestions, analyze_document
from document_editor import apply_changes, clear_changes, accept_changes, move_cursor, get_document_content
import json

load_dotenv()

app = FastAPI()

class AudioData(BaseModel):
    audio: str

class DocumentUpdate(BaseModel):
    document_id: str
    content: list

class CursorMove(BaseModel):
    document_id: str
    direction: str
    steps: int = 1

class WordSearch(BaseModel):
    document_id: str
    words: str

active_connections = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get('action')
            if action == 'processAudio':
                audio_data = data.get('audio')
                transcript = process_voice(audio_data)
                command = detect_voice_commands(transcript)
                if command:
                    await handle_voice_command(websocket, command)
                else:
                    suggestions = generate_suggestions(transcript)
                    await websocket.send_json({
                        'type': 'transcript',
                        'content': transcript
                    })
                    await websocket.send_json({
                        'type': 'suggestions',
                        'content': suggestions
                    })
            elif action == 'updateDocument':
                document_id = data.get('document_id')
                content = data.get('content')
                update_result = apply_changes(document_id, content)
                await websocket.send_json({
                    'type': 'updateResult',
                    'content': update_result
                })
            elif action == 'analyzeDocument':
                document_id = data.get('document_id')
                document_content = get_document_content(document_id)
                analysis = analyze_document(document_content)
                await websocket.send_json({
                    'type': 'documentAnalysis',
                    'content': analysis
                })
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def handle_voice_command(websocket: WebSocket, command: str):
    if command.startswith("move cursor"):
        direction = command.split()[-1]
        await move_cursor_ws(websocket, direction)
    elif command == "clear markup":
        await clear_changes_ws(websocket)
    elif command == "accept suggested":
        await accept_changes_ws(websocket)
    elif command == "make suggestion":
        await generate_suggestions_ws(websocket)
    else:
        await websocket.send_json({
            'type': 'commandResult',
            'content': f"Unrecognized command: {command}"
        })

async def move_cursor_ws(websocket: WebSocket, direction: str):
    result = move_cursor(direction)
    await websocket.send_json({
        'type': 'cursorMove',
        'content': result
    })

async def clear_changes_ws(websocket: WebSocket):
    result = clear_changes()
    await websocket.send_json({
        'type': 'changesClear',
        'content': result
    })

async def accept_changes_ws(websocket: WebSocket):
    result = accept_changes()
    await websocket.send_json({
        'type': 'changesAccepted',
        'content': result
    })

async def generate_suggestions_ws(websocket: WebSocket):
    document_content = get_document_content()
    suggestions = generate_suggestions(document_content)
    await websocket.send_json({
        'type': 'suggestions',
        'content': suggestions
    })

@app.post("/update_document")
async def update_document(update: DocumentUpdate):
    result = apply_changes(update.document_id, update.content)
    return {"status": "success", "result": result}

@app.post("/move_cursor")
async def move_document_cursor(move: CursorMove):
    result = move_cursor(move.document_id, move.direction, move.steps)
    return {"status": "success", "result": result}

@app.post("/search_words")
async def search_words(search: WordSearch):
    result = move_cursor(search.document_id, search.words)
    return {"status": "success", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)