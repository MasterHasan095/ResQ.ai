from typing import Optional
from pydantic import BaseModel

class AnalyzeResponse(BaseModel):
    fall_detected: bool
    confidence: float
    severity: Optional[str] = None
