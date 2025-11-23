# app/routers/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/falls")
async def websocket_falls(websocket: WebSocket):
    """
    Clients connect here to receive live fall alerts.
    For now it's a simple broadcast channel (no rooms).
    """
    await manager.connect(websocket)
    try:
        # We don't really *need* to receive anything from the client yet;
        # just keep the connection alive.
        while True:
            # This will block until client sends something or disconnects.
            # You can also use websocket.receive_text() if you want to handle messages.
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
