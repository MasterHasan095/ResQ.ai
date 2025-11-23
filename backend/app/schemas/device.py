from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Device(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    platform: str
    push_token: Optional[str] = None
    nickname: Optional[str] = None
    last_seen_at: Optional[datetime] = None
    active: bool
    created_at: datetime
