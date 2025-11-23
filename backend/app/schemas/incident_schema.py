# backend/app/schemas/incident_schema.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class IncidentBase(BaseModel):
    fall_detected: bool
    confidence: float
    severity: Optional[str] = None
    device_id: Optional[str] = None


class IncidentRead(IncidentBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
