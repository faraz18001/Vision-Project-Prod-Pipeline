"""
Create CVAT-ready zip file from auto-labeling output.
Run this after running the auto_labeling notebook.
"""

import os
import shutil
import zipfile

# Paths - adjust if needed
PROJECT_ROOT = r"c:/Users/Tesla Laptops/Videos/Construction-Site-Safety-PPE-Detection"
OUTPUT_FOLDER = f"{PROJECT_ROOT}/auto_labels"

# Output folder for CVAT package
cvat_folder = f"{OUTPUT_FOLDER}/cvat_package"
if os.path.exists(cvat_folder):
    shutil.rmtree(cvat_folder)
os.makedirs(cvat_folder)

# Class names (only positive classes, matching filtered class IDs)
# Original model classes: 0=Hardhat, 1=Mask, 5=Person, 6=Safety Cone, 7=Safety Vest, 8=machinery, 9=vehicle, 10=Chair
class_names = [
    "Hardhat",  # 0
    "Mask",  # 1
    "Person",  # 2 (was 5)
    "Safety Cone",  # 3 (was 6)
    "Safety Vest",  # 4 (was 7)
    "machinery",  # 5 (was 8)
    "vehicle",  # 6 (was 9)
    "Chair",  # 7 (was 10)
]

# Mapping from original class IDs to new sequential IDs
# Since we filtered with classes=[0, 1, 5, 6, 7, 8, 9, 10], YOLO outputs original IDs
# We need to remap them to sequential 0-7 for CVAT
class_mapping = {
    0: 0,  # Hardhat -> 0
    1: 1,  # Mask -> 1
    5: 2,  # Person -> 2
    6: 3,  # Safety Cone -> 3
    7: 4,  # Safety Vest -> 4
    8: 5,  # machinery -> 5
    9: 6,  # vehicle -> 6
    10: 7,  # Chair -> 7
}

# Create obj.names
with open(f"{cvat_folder}/obj.names", "w") as f:
    for name in class_names:
        f.write(name + "\n")
print(f"Created obj.names with {len(class_names)} classes")

# Create obj.data
with open(f"{cvat_folder}/obj.data", "w") as f:
    f.write(f"classes = {len(class_names)}\n")
    f.write("names = obj.names\n")
print("Created obj.data")

# Copy and remap labels
labels_src = f"{OUTPUT_FOLDER}/predictions/labels"
labels_dst = f"{cvat_folder}/labels"
os.makedirs(labels_dst, exist_ok=True)

if os.path.exists(labels_src):
    label_files = os.listdir(labels_src)
    for label_file in label_files:
        src_path = os.path.join(labels_src, label_file)
        dst_path = os.path.join(labels_dst, label_file)

        # Read and remap class IDs
        with open(src_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                old_class_id = int(parts[0])
                if old_class_id in class_mapping:
                    new_class_id = class_mapping[old_class_id]
                    parts[0] = str(new_class_id)
                    new_lines.append(" ".join(parts) + "\n")

        # Write remapped labels
        with open(dst_path, "w") as f:
            f.writelines(new_lines)

    print(f"Copied and remapped {len(label_files)} label files")
else:
    print("No labels folder found!")

# Create zip file
zip_path = f"{OUTPUT_FOLDER}/cvat_upload.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(cvat_folder):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, cvat_folder)
            zipf.write(file_path, arcname)

print(f"\nCVAT-ready zip created: {zip_path}")
print(f"\nContents:")
print(f"  - obj.names ({len(class_names)} classes)")
print(f"  - obj.data")
print(f"  - labels/ folder")
print(f"\nUpload this zip directly to CVAT!")
print(f"\nCVAT Labels JSON (paste in Raw mode):")
print("[")
for i, name in enumerate(class_names):
    comma = "," if i < len(class_names) - 1 else ""
    print(f'  {{"name": "{name}", "type": "rectangle", "attributes": []}}{comma}')
print("]")
