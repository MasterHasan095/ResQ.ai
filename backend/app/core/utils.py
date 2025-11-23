# backend/app/core/utils.py

import numpy as np

def calculate_angle(p1, p2, p3):
    """
    Returns angle at p2 formed by p1–p2–p3 (in degrees).
    """
    a = np.array(p1) - np.array(p2)
    b = np.array(p3) - np.array(p2)

    # Avoid division by zero
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0

    cos_theta = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    # Clip values to avoid domain error
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    return np.degrees(np.arccos(cos_theta))


def normalize_keypoints(keypoints: np.ndarray, height: int) -> np.ndarray:
    """
    Normalize Y values by frame height (optional for DS enhancements).
    """
    keypoints_norm = keypoints.copy()
    keypoints_norm[:, 1] = keypoints_norm[:, 1] / height
    return keypoints_norm
