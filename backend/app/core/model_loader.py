# backend/app/core/model_loader.py

from ultralytics import YOLO
from pathlib import Path
import threading

_yolo_model = None
_model_lock = threading.Lock()

def get_yolo_model():
    """
    Lazy-load YOLO Pose model (yolov8/11).
    Ensures only one instance loads into memory.
    """
    global _yolo_model

    if _yolo_model is None:
        with _model_lock:
            if _yolo_model is None:  # double-check
                weights_path = (
                    Path(__file__).resolve().parent.parent
                    / "models"
                    / "yolov8n-pose.pt"
                )
                print(f"[Model Loader] Loading YOLO Pose model from {weights_path}")
                _yolo_model = YOLO(str(weights_path))

    return _yolo_model
