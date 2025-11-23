from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Notification(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    incident_id: str
    contact_id: str
    channel: str            # sms / call / whatsapp / push
    status: str             # pending / sent / failed
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
