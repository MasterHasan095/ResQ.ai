# backend/app/routers/analyze.py

from typing import Optional

import cv2
import numpy as np
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status,
)

from app.schemas.analyze_schema import AnalyzeResponse
from app.core.pose_inference import run_pose_inference
from app.core.fall_logic import FallDetector
from app.database.incident_logger import log_incident

# This router gets prefixed in main.py: prefix="/analyze"
router = APIRouter()

fall_detector = FallDetector()


@router.get("/ping")
def ping():
    # GET /analyze/ping → quick health check for this router
    return {"analyze": "ok"}


@router.post("/frame", response_model=AnalyzeResponse)
async def analyze_frame(
    file: UploadFile = File(...),
    device_id: Optional[str] = None,          # Flutter can send ?device_id=phone123
):
    # 1) Validate file type
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type",
        )

    # 2) Read uploaded image into OpenCV BGR frame
    data = await file.read()
    np_arr = np.frombuffer(data, np.uint8)
    frame_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame_bgr is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not decode image",
        )

    # 3) Run pose inference (Priyanshu's function)
    keypoints_list = run_pose_inference(frame_bgr)  # list[np.ndarray]
    first_person = keypoints_list[0] if keypoints_list else None

    # 4) Run fall detection (Priyanshu's logic)
    if first_person is None:
        fall_flag = False
        confidence = 0.0
    else:
        result = fall_detector.update(first_person)
        fall_flag = bool(result.get("fall", False))
        confidence = float(result.get("confidence", 0.0))

    # 5) Simple severity rule based on confidence
    if confidence >= 0.8:
        severity = "high"
    elif confidence >= 0.5:
        severity = "medium"
    else:
        severity = "low"

    # 6) Log incident in MongoDB ONLY if a fall is detected
    if fall_flag:
        log_incident(
            {
                "device_id": device_id,
                "fall_detected": fall_flag,
                "confidence": confidence,
                "severity": severity,
            }
        )

    # 7) Return clean JSON for Flutter
    return AnalyzeResponse(
        fall_detected=fall_flag,
        confidence=confidence,
        severity=severity,
    )
