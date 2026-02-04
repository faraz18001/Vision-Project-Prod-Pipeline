import os
import shutil
import zipfile

# CONFIGURATION
PROJECT_ROOT = r"c:/Users/Tesla Laptops/Videos/Construction-Site-Safety-PPE-Detection"
IMAGES_DIR = f"{PROJECT_ROOT}/new_images"
LABELS_DIR = f"{PROJECT_ROOT}/sam_labels/labels"
OUTPUT_ZIP = f"{PROJECT_ROOT}/roboflow_upload.zip"

# The names of your classes in order (0, 1, 2...)
CLASS_NAMES = [
    "Hardhat",
    "Mask",
    "NO-Hardhat",
    "NO-Mask",
    "NO-Safety Vest",
    "Person",
    "Safety Cone",
    "Safety Vest",
    "machinery",
    "vehicle",
]


def main():
    print("Preparing Roboflow Upload Package...")

    # Create a temporary directory for zipping
    temp_dir = f"{PROJECT_ROOT}/temp_roboflow"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.makedirs(f"{temp_dir}/images")
    os.makedirs(f"{temp_dir}/labels")

    # Create classes.txt (The Labelmap) inside the labels folder
    with open(os.path.join(temp_dir, "labels", "classes.txt"), "w") as f:
        for name in CLASS_NAMES:
            f.write(name + "\n")

    # 1. Copy Images
    img_count = 0
    for img in os.listdir(IMAGES_DIR):
        if img.lower().endswith((".jpg", ".jpeg", ".png")):
            shutil.copy2(
                os.path.join(IMAGES_DIR, img), os.path.join(temp_dir, "images", img)
            )
            img_count += 1

    # 2. Copy Labels
    lbl_count = 0
    for lbl in os.listdir(LABELS_DIR):
        if lbl.endswith(".txt"):
            shutil.copy2(
                os.path.join(LABELS_DIR, lbl), os.path.join(temp_dir, "labels", lbl)
            )
            lbl_count += 1

    # 3. Create Zip
    print(
        f"Zipping {img_count} images and {lbl_count} labels (including classes.txt)..."
    )
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)

    # Cleanup
    shutil.rmtree(temp_dir)
    print(f"\nSUCCESS! Created: {OUTPUT_ZIP}")
    print("Now just DRAG AND DROP this zip file into Roboflow.")


if __name__ == "__main__":
    main()
