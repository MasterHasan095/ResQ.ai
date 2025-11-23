import cv2
import numpy as np
from app.core.pose_inference import run_pose_inference
from app.core.fall_logic import FallDetector

# Initialize fall detector with tunable sensitivity
fall_detector = FallDetector(
    max_history=15,
    drop_threshold_norm=0.30,   # try 0.25–0.35
    gap_threshold_norm=0.22     # try 0.18–0.25
)

def main():
    # -----------------------------------------------
    # SELECT INPUT MODE
    # -----------------------------------------------
    USE_WEBCAM = True   # ▶️ change to True for webcam mode

    if USE_WEBCAM:
        print("Using webcam...")
        cap = cv2.VideoCapture(0)
    else:
        video_path = "videos/testvideo4.mp4"
        print(f"Using video file: {video_path}")
        cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Failed to open source!")
        return

    print("Processing... Press ESC or Q to stop.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No frame received (video ended or camera error).")
            break

        # Run pose inference
        poses = run_pose_inference(frame)

        if len(poses) == 0:
            print("No pose detected")
        else:
            keypoints = poses[0]

            print("Keypoints shape:", keypoints.shape)

            # Fall detection
            result = fall_detector.update(keypoints)
            print("Result:", result)

            # Draw result on frame
            text = f"Fall: {result['fall']} | Conf: {result['confidence']:.2f}"
            cv2.putText(
                frame,
                text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255) if result["fall"] else (0, 255, 0),
                2
            )

            # Draw keypoints
            for (x, y) in keypoints:
                cv2.circle(frame, (int(x), int(y)), 4, (255, 0, 0), -1)

        cv2.imshow("YOLO Pose + Fall Detection", frame)

        # -------------------------------
        # EXIT CONDITIONS (ESC OR Q KEY)
        # -------------------------------
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):     # 27 = ESC, 'q' = quit
            print("Exit key pressed. Stopping...")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
