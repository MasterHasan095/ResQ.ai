# backend/app/core/fall_logic.py

import numpy as np
from collections import deque

# COCO keypoint indexes for YOLOv8 pose (17-keypoint model)
# 0: nose
# 5: left shoulder, 6: right shoulder
# 11: left hip,     12: right hip
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6
LEFT_HIP = 11
RIGHT_HIP = 12


class FallDetector:
    def __init__(
        self,
        max_history: int = 15,
        drop_threshold_norm: float = 0.35,
        gap_threshold_norm: float = 0.18,
    ):
        """
        max_history:
            How many frames to keep in history.
        drop_threshold_norm:
            Minimum normalized hip drop (as a fraction of body height) to consider a fall.
        gap_threshold_norm:
            Maximum normalized shoulder-hip gap after fall (lying posture).
        """
        self.history = deque(maxlen=max_history)
        self.drop_threshold_norm = drop_threshold_norm
        self.gap_threshold_norm = gap_threshold_norm

    def _compute_body_height(self, keypoints: np.ndarray) -> float:
        ys = keypoints[:, 1]
        body_h = float(ys.max() - ys.min())
        return body_h if body_h > 1.0 else 1.0  # avoid division by zero

    def _compute_hip_center_y(self, keypoints: np.ndarray) -> float:
        return float((keypoints[LEFT_HIP][1] + keypoints[RIGHT_HIP][1]) / 2.0)

    def _compute_shoulder_center_y(self, keypoints: np.ndarray) -> float:
        return float((keypoints[LEFT_SHOULDER][1] + keypoints[RIGHT_SHOULDER][1]) / 2.0)

    def update(self, keypoints: np.ndarray | None) -> dict:
        """
        Update with new keypoints and detect fall.

        Args:
            keypoints: np.ndarray with shape (num_keypoints, 2)

        Returns:
            dict: {"fall": bool, "confidence": float}
        """

        # No detection or too few keypoints → we can't reason.
        if keypoints is None or keypoints.shape[0] < 13:
            return {"fall": False, "confidence": 0.0}

        # We are assuming COCO-style indexing, so if these indexes are out of range, bail.
        num_kpts = keypoints.shape[0]
        needed_idxs = [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_HIP, RIGHT_HIP]
        if any(idx >= num_kpts for idx in needed_idxs):
            return {"fall": False, "confidence": 0.0}

        body_h = self._compute_body_height(keypoints)
        hip_y = self._compute_hip_center_y(keypoints)
        shoulder_y = self._compute_shoulder_center_y(keypoints)

        # Save to history
        self.history.append(
            {
                "hip_y": hip_y,
                "shoulder_y": shoulder_y,
                "body_h": body_h,
            }
        )

        # Need at least a few frames to reason
        if len(self.history) < 5:
            return {"fall": False, "confidence": 0.0}

        # ---- 1) Compute normalized hip drop over a short window ----
        # Compare current hips to hips a few frames ago
        window = min(20, len(self.history) - 1)
        prev_hip_y = self.history[-1 - window]["hip_y"]
        curr_hip_y = self.history[-1]["hip_y"]

        # In image coordinates, DOWNWARD movement = hip_y increases.
        raw_drop = curr_hip_y - prev_hip_y  # positive if moved down

        # Normalize by current body height
        drop_norm = raw_drop / body_h

        # ---- 2) Compute shoulder-hip gap (standing vs lying) ----
        gap = hip_y - shoulder_y  # how much hips are below shoulders
        gap_norm = gap / body_h   # normalized

        # When standing, gap_norm is relatively large.
        # When lying, shoulders and hips are closer vertically → gap_norm smaller.

        # ---- 3) Decide if it's a fall ----
        drop_ok = drop_norm > self.drop_threshold_norm
        posture_ok = gap_norm < self.gap_threshold_norm  # looks "flattened"

        fall_detected = drop_ok and posture_ok

        if not fall_detected:
            return {"fall": False, "confidence": 0.0}

        # ---- 4) Compute a rough confidence score ----
        # Higher hip drop and "flatter" posture → higher confidence
        drop_score = min(1.0, drop_norm / self.drop_threshold_norm)
        posture_score = min(1.0, (self.gap_threshold_norm - gap_norm) / self.gap_threshold_norm)
        posture_score = max(0.0, posture_score)

        confidence = 0.5 * drop_score + 0.5 * posture_score
        confidence = float(max(0.0, min(1.0, confidence)))

        return {"fall": True, "confidence": confidence}
