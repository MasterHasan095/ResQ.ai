from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.analyze_schema import AnalyzeResponse

import cv2
import numpy as np

from app.core.pose_inference import run_pose_inference
from app.core.fall_logic import FallDetector

from app.database.incident_logger import log_incident


router = APIRouter()
fall_detector = FallDetector()


@router.get("/ping")
def ping():
    return {"analyze": "ok"}

@router.post("/frame", response_model=AnalyzeResponse)
async def analyze_frame(file: UploadFile = File(...)):

    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Unsupported file type")


    # Read image bytes
    data = await file.read()
    np_arr = np.frombuffer(data, np.uint8)
    frame_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame_bgr is None:
        raise HTTPException(status_code=400, detail="Could not decode image")

    # 3) run pose + fall logic
    keypoints_list = run_pose_inference(frame_bgr)  # list of np.ndarray
    first_person = keypoints_list[0] if keypoints_list else None

    result = fall_detector.update(first_person) if first_person is not None else {
        "fall": False,
        "confidence": 0.0,
    }

    if result.get("fall"):
        log_incident(result)

    return AnalyzeResponse(
        fall_detected=bool(result.get("fall", False)),
        confidence=float(result.get("confidence", 0.0)),
    )
