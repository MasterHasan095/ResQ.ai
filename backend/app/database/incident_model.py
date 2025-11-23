# backend/app/database/incident_model.py

from datetime import datetime
from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    fall_detected: bool
    confidence: float
    severity: str | None = None
    device_id: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class IncidentRead(BaseModel):
    id: str
    fall_detected: bool
    confidence: float
    severity: str | None
    device_id: str | None
    timestamp: datetime
