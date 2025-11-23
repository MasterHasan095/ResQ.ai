# app/core/detector_loop.py
import asyncio
import cv2
import numpy as np

from app.core.pose_inference import run_pose_inference
from app.core.fall_logic import FallDetector
from app.core.alerts import handle_fall_event   # async


fall_detector = FallDetector(
    max_history=15,
    drop_threshold_norm=0.30,
    gap_threshold_norm=0.22
)


async def detection_loop():
    """
    Long-running async task that:
    - reads frames from webcam/video
    - runs pose inference
    - updates fall detector
    - on a new fall, calls handle_fall_event(...)
    """

    USE_WEBCAM = True

    if USE_WEBCAM:
        print("Using webcam...")
        source_label = "webcam_0"
        cap = cv2.VideoCapture(0)
    else:
        video_path = "videos/testvideo4.mp4"
        print(f"Using video: {video_path}")
        source_label = video_path
        cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Failed to open video/camera")
        return

    print("Processing... (server mode)\n")

    prev_fall = False   # Track fall change
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Video ended or camera error")
            break

        frame_idx += 1

        poses = run_pose_inference(frame)

        if len(poses) == 0:
            prev_fall = False  # Reset if no person
        else:
            keypoints = poses[0]

            result = fall_detector.update(keypoints)

            # 🔥 FIRE EVENT ONLY ON transition: False -> True
            if result["fall"] and not prev_fall:
                await handle_fall_event(
                    result,
                    keypoints,
                    metadata={
                        "frame_idx": frame_idx,
                        "source": source_label,
                        "resolution": (frame.shape[1], frame.shape[0]),
                    },
                )

            prev_fall = result["fall"]

            # Optional: overlay (for debugging if you have a screen)
            text = f"Fall: {result['fall']} | Conf: {result['confidence']:.2f}"
            cv2.putText(
                frame,
                text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255) if result["fall"] else (0, 255, 0),
                2,
            )

            for (x, y) in keypoints:
                cv2.circle(frame, (int(x), int(y)), 4, (255, 0, 0), -1)

        # You *can* keep this if you want a debug window while server runs
        cv2.imshow("YOLO Pose + Fall Detection", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            break

        # Yield to event loop so FastAPI doesn't starve
        await asyncio.sleep(0)

    cap.release()
    cv2.destroyAllWindows()
