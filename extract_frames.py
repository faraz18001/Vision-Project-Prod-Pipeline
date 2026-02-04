import cv2
import os
import glob
import sys

# CONFIGURATION
INPUT_DIR = r"1_raw_footage"
OUTPUT_DIR = r"2_processed_images"
FRAME_INTERVAL = (
    30  # Save 1 frame every X frames (e.g., 30 = 1 per second for 30fps video)
)


def extract_frames():
    print(f"--- Frame Extractor ---")

    # Create output dir if not exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Find Videos
    extensions = ["*.mp4", "*.avi", "*.mov", "*.mkv"]
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(INPUT_DIR, ext)))

    if not files:
        print(f"No video files found in '{INPUT_DIR}'")
        return

    print(f"Found {len(files)} videos to process.")

    total_saved = 0

    for video_path in files:
        cap = cv2.VideoCapture(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        print(f"Processing: {video_name}...")

        frame_count = 0
        saved_count = 0

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            if frame_count % FRAME_INTERVAL == 0:
                # Save frame
                out_name = f"{video_name}_frame_{frame_count:06d}.jpg"
                out_path = os.path.join(OUTPUT_DIR, out_name)
                cv2.imwrite(out_path, frame)
                saved_count += 1
                total_saved += 1

            frame_count += 1

        cap.release()
        print(f"  -> Extracted {saved_count} frames.")

    print(f"Done! Total {total_saved} images saved to '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    extract_frames()
