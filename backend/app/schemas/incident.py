from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class IncidentBase(BaseModel):
    user_id: str
    device_id: Optional[str] = None
    fall_detected: bool
    confidence: float
    severity: str               # low / medium / high
    timestamp: datetime
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    was_canceled_by_user: Optional[bool] = None
    notes: Optional[str] = None


class IncidentCreate(IncidentBase):
    pass


class IncidentRead(IncidentBase):
    id: Optional[str] = Field(default=None, alias="_id")

    class Config:
      populate_by_name = True
