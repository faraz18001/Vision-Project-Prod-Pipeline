import cv2
from ultralytics import YOLO
import os
import glob
import sys

# CONFIGURATION
PROJECT_ROOT = r"c:/Users/Tesla Laptops/Videos/Construction-Site-Safety-PPE-Detection"
MODELS_DIR = f"{PROJECT_ROOT}/models"
FOOTAGE_DIR = f"{PROJECT_ROOT}/footage"


def get_latest_file(directory, extensions):
    files = []
    for ext in extensions:
        files.extend(glob.glob(f"{directory}/*{ext}"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def main():
    print("--- PPE Detection Video Runner ---")

    # 1. Find Model
    # Look for best.pt first, otherwise take the newest .pt file
    model_path = os.path.join(MODELS_DIR, "best.pt")
    if not os.path.exists(model_path):
        print(
            f" 'best.pt' not found in models folder. Searching for newest .pt file..."
        )
        model_path = get_latest_file(MODELS_DIR, [".pt"])

    if not model_path:
        print(f"ERROR: No model (.pt) files found in {MODELS_DIR}")
        sys.exit(1)

    print(f"Loading Model: {os.path.basename(model_path)}")
    model = YOLO(model_path)

    # 2. Find Video
    video_path = get_latest_file(FOOTAGE_DIR, [".mp4", ".avi", ".mov", ".mkv"])
    if not video_path:
        print(f"ERROR: No video files found in {FOOTAGE_DIR}")
        print("Please put a video file (.mp4, .avi) inside the 'footage' folder.")
        sys.exit(1)

    print(f"Processing Video: {os.path.basename(video_path)}")

    # 3. Run Inference
    cap = cv2.VideoCapture(video_path)

    # Get video info for resizing windows if needed
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = 1.0
    if height > 1000:
        scale = 0.5

    cv2.namedWindow("PPE Detection", cv2.WINDOW_NORMAL)
    if scale != 1.0:
        cv2.resizeWindow("PPE Detection", int(width * scale), int(height * scale))

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("End of video.")
            break

        # Run YOLO prediction
        # conf=0.5 means only show boxes with >50% confidence
        results = model.predict(frame, conf=0.5, verbose=False)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the frame
        cv2.imshow("PPE Detection", annotated_frame)

        # Break loop if 'q' or 'ESC' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
