from datetime import datetime

def log_incident(data: dict) -> None:
    """
    Temporary stub: later this will write to DB.
    For now it just prints so we can see it's being called.
    """
    incident = {
        "timestamp": datetime.utcnow().isoformat(),
        "fall_detected": bool(data.get("fall", False)),
        "confidence": float(data.get("confidence", 0.0)),
    }
    print("INCIDENT LOG:", incident)
