# app/core/alerts.py
from datetime import datetime
import numpy as np

def serialize_keypoints(keypoints):
    """Convert to JSON-safe structure."""
    try:
        return keypoints.tolist()
    except:
        return [list(map(float, p)) for p in keypoints]

def handle_fall_event(result, keypoints, metadata=None):
    """
    Called ONLY when a new fall is detected.
    This is where Twilio + WebSocket will integrate later.
    """

    event = {
        "event": "fall_detected",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "fall": result.get("fall", True),
        "confidence": float(result.get("confidence", 0.0)),
        "keypoints": serialize_keypoints(keypoints),
        "metadata": metadata or {},
    }

    # TODO: Twilio SMS
    # send_fall_sms(event)

    # TODO: WebSocket push
    # await ws_manager.broadcast_json(event)

    print("\n🔥🔥 FALL DETECTED 🔥🔥")
    print(event)
    print("--------------------------------------------------\n")
