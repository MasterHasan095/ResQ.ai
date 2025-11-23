from pydantic import BaseModel

class AnalyzeResponse(BaseModel):
    fall_detected: bool
    confidence: float
