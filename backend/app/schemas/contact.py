from pydantic import BaseModel, Field
from typing import Optional

class Contact(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    name: str
    relationship: Optional[str] = None
    phone: str
    email: Optional[str] = None
    preferred_channel: Optional[str] = None
