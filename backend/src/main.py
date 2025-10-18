"""FastAPI application entry point."""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, status as http_status
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Set
from uuid import UUID

from backend.src.config import settings
from backend.src.api.routes import auth, project, session, message, profile
from backend.src.auth.jwt_handler import JWTHandler
from backend.src.repositories import UserRepository
from backend.src.database import get_db

# Create FastAPI application
app = FastAPI(
    title="Socrates 8.0 API",
    description="AI-powered Socratic questioning system",
    version="8.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(auth.router, prefix="/api")
app.include_router(project.router, prefix="/api")
app.include_router(session.router, prefix="/api")
app.include_router(message.router, prefix="/api")
app.include_router(profile.router, prefix="/api")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        # Store active connections: {session_id: Set[WebSocket]}
        self.active_connections: dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect a WebSocket to a session."""
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()
        self.active_connections[session_id].add(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        """Disconnect a WebSocket from a session."""
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, session_id: str, message: dict):
        """Broadcast a message to all connections in a session."""
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    # Connection might be closed
                    pass

    async def notify_typing(self, session_id: str, user_id: str, is_typing: bool):
        """Notify about typing status."""
        message = {
            "type": "typing",
            "user_id": user_id,
            "is_typing": is_typing
        }
        await self.broadcast(session_id, message)

    async def notify_message(self, session_id: str, message_data: dict):
        """Notify about new message."""
        notification = {
            "type": "message",
            "data": message_data
        }
        await self.broadcast(session_id, notification)


manager = ConnectionManager()


# WebSocket endpoint
@app.websocket("/ws/sessions/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time session communication."""
    # Get token from query params
    token = None
    if websocket.query_params.get("token"):
        token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=http_status.WS_1008_POLICY_VIOLATION, reason="No token")
        return

    # Verify token
    user_id = JWTHandler.verify_token(token)
    if not user_id:
        await websocket.close(code=http_status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        return

    # Connect to session
    await manager.connect(websocket, session_id)

    try:
        # Notify others that user is online
        await manager.broadcast(session_id, {
            "type": "user_joined",
            "user_id": user_id,
            "message": f"User {user_id} joined the session"
        })

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle different message types
            if message.get("type") == "typing":
                await manager.notify_typing(session_id, user_id, message.get("is_typing", False))

            elif message.get("type") == "message":
                # Broadcast message to all connected clients
                await manager.notify_message(session_id, {
                    "user_id": user_id,
                    "content": message.get("content"),
                    "timestamp": message.get("timestamp")
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
        await manager.broadcast(session_id, {
            "type": "user_left",
            "user_id": user_id,
            "message": f"User {user_id} left the session"
        })
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, session_id)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "8.0.0"
    }


@app.get("/api/status")
async def api_status():
    """Detailed API status."""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "8.0.0",
        "environment": settings.ENVIRONMENT,
        "websocket": "enabled"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
