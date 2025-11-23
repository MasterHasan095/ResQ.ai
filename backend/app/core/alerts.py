# app/core/alerts.py
from datetime import datetime
import numpy as np
import asyncio

from app.core.websocket_manager import manager  # ⬅ NEW


def serialize_keypoints(keypoints):
    """Convert to JSON-safe structure."""
    try:
        return keypoints.tolist()
    except Exception:
        return [list(map(float, p)) for p in keypoints]


async def handle_fall_event(result, keypoints, metadata=None):
    """
    Called ONLY when a new fall is detected.
    This is where Twilio + WebSocket will integrate later.
    """

    event = {
        "event": "fall_detected",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "fall": bool(result.get("fall", True)),
        "confidence": float(result.get("confidence", 0.0)),
        "keypoints": serialize_keypoints(keypoints),
        "metadata": metadata or {},
    }

    # TODO: Twilio SMS
    # await send_fall_sms(event)  # make that async later

    # 🔌 WebSocket push
    # if we are in an async context, we can await directly;
    # if not, we'll schedule on the event loop.
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(manager.broadcast_json(event))
    except RuntimeError:
        # No running loop (e.g., called from sync context), fall back
        asyncio.run(manager.broadcast_json(event))

    print("\n🔥🔥 FALL DETECTED 🔥🔥")
    print(event)
    print("--------------------------------------------------\n")
