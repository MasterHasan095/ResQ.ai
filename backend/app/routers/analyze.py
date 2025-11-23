from fastapi import APIRouter, UploadFile, File
from app.schemas.analyze_schema import AnalyzeResponse
import cv2
import numpy as np

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "analyze router working"}

@router.post("/frame", response_model=AnalyzeResponse)
async def analyze_frame(file: UploadFile = File(...)):
    # Read image bytes
    data = await file.read()
    nparr = np.frombuffer(data, np.uint8)

    # Decode into OpenCV frame (BGR)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # TODO: integrate Priyanshu's AI here:
    # from app.core.main_ai import analyze_frame
    # result = analyze_frame(frame)

    # Dummy result for now
    return AnalyzeResponse(
        fall_detected=False,
        confidence=0.0
    )
