# backend/app/core/pose_inference.py

import numpy as np
import cv2
from .model_loader import get_yolo_model

def run_pose_inference(frame_bgr: np.ndarray) -> list[np.ndarray]:
    """
    Run YOLO pose inference on an OpenCV BGR frame.
    Returns:
        list of (num_keypoints x 2) numpy arrays for each detected person.
    """
    model = get_yolo_model()
    results = model(frame_bgr)

    poses: list[np.ndarray] = []

    for r in results:
        if r.keypoints is None:
            continue

        # r.keypoints.xy shape: (num_persons, num_keypoints, 2)
        kp = r.keypoints.xy
        if kp is None:
            continue

        kp_np = kp.cpu().numpy()

        for person_kpts in kp_np:
            # person_kpts shape: (num_keypoints, 2)
            poses.append(person_kpts)

    return poses
