from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    phone: str
    email: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    risk_level: str               # low / medium / high
    medical_notes: Optional[str] = None
    created_at: datetime
