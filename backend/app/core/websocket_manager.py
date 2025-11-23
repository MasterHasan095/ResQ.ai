# app/core/websocket_manager.py
from typing import List
from fastapi import WebSocket, WebSocketDisconnect
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def send_json(self, data, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast_json(self, data):
        """
        Send a JSON message to all connected clients.
        If any connection is dead, drop it.
        """
        async with self._lock:
            connections = list(self.active_connections)

        for ws in connections:
            try:
                await ws.send_json(data)
            except Exception:
                # Connection is probably dead, remove it
                await self.disconnect(ws)


# Single global manager instance
manager = ConnectionManager()
