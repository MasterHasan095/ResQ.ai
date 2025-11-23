# backend/app/routers/analyze.py

from typing import Optional

import cv2
import numpy as np
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.schemas.analyze_schema import AnalyzeResponse
from app.core.pose_inference import run_pose_inference
from app.core.fall_logic import FallDetector
from app.database.db import get_db
from app.database.incident_model import Incident
from app.notifications.sms import send_fall_alert_sms  # 👈 import your SMS helper

router = APIRouter(
    prefix="/analyze",
    tags=["analyze"],
)

fall_detector = FallDetector()


@router.get("/ping")
def ping():
    return {"analyze": "ok"}


@router.post("/frame", response_model=AnalyzeResponse)
async def analyze_frame(
    file: UploadFile = File(...),
    device_id: Optional[str] = None,
    db: Session = Depends(get_db),
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

    # 4) Run fall detection
    if first_person is None:
        fall_flag = False
        confidence = 0.0
    else:
        result = fall_detector.update(first_person)
        fall_flag = bool(result.get("fall", False))
        confidence = float(result.get("confidence", 0.0))

    # 5) Severity based on confidence
    if confidence >= 0.8:
        severity = "high"
    elif confidence >= 0.5:
        severity = "medium"
    else:
        severity = "low"

    # 6) Log incident in DB ONLY if a fall is detected
    if fall_flag:
        incident = Incident(
            fall_detected=fall_flag,
            confidence=confidence,
            severity=severity,
            device_id=device_id,
        )
        db.add(incident)
        db.commit()
        db.refresh(incident)

        # 7) 🔔 Send real SMS alert using Twilio
        # For now, hard-code one emergency contact for demo:
        EMERGENCY_PHONE = "+19055987068"   # 👈 put your verified phone number here
        PATIENT_NAME = "Yashika"      # 👈 or "Ishan", or get from DB later

        try:
            send_fall_alert_sms(
                to_phone=EMERGENCY_PHONE,
                patient_name=PATIENT_NAME,
                severity=severity,
                confidence=confidence,
            )
        except Exception as e:
            # don't crash the API if SMS fails, just log it
            print(f"❌ Error sending SMS: {e}")

    # 8) Return clean JSON for Flutter / testing
    return AnalyzeResponse(
        fall_detected=fall_flag,
        confidence=confidence,
        severity=severity,
    )
