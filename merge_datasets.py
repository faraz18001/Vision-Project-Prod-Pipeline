import os
import shutil
from pathlib import Path

def merge_datasets():
    base_path = Path("c:/Users/Tesla Laptops/Videos/Construction-Site-Safety-PPE-Detection")
    ppe_path = base_path / "constructiondataset"
    chair_path = base_path / "chair-dataset"
    merged_path = base_path / "merged-dataset"

    # Create directory structure for merged dataset
    for split in ['train', 'valid', 'test']:
        (merged_path / split / 'images').mkdir(parents=True, exist_ok=True)
        (merged_path / split / 'labels').mkdir(parents=True, exist_ok=True)

    print("Starting merge process...")

    # 1. Copy PPE dataset (preserving classes 0-9)
    for split in ['train', 'valid', 'test']:
        ppe_split_img = ppe_path / split / 'images'
        ppe_split_lbl = ppe_path / split / 'labels'
        
        if not ppe_split_img.exists():
            continue

        print(f"Copying PPE {split} files...")
        for img_file in ppe_split_img.glob('*'):
            shutil.copy(img_file, merged_path / split / 'images')
            
            lbl_file = ppe_split_lbl / f"{img_file.stem}.txt"
            if lbl_file.exists():
                shutil.copy(lbl_file, merged_path / split / 'labels')

    # 2. Copy Chair dataset and offset class 0 to class 10
    # Chair dataset only has 'train' folder
    chair_train_img = chair_path / 'train' / 'images'
    chair_train_lbl = chair_path / 'train' / 'labels'

    if chair_train_img.exists():
        print("Copying and offsetting Chair training files...")
        images = list(chair_train_img.glob('*'))
        
        # We'll split chair data: 80% train, 20% validation
        split_idx = int(len(images) * 0.8)
        
        for i, img_file in enumerate(images):
            # Determine target split
            target_split = 'train' if i < split_idx else 'valid'
            
            # Copy image
            # Rename image to avoid name collisions if any
            new_img_name = f"chair_{img_file.name}"
            shutil.copy(img_file, merged_path / target_split / 'images' / new_img_name)
            
            # Process label
            lbl_file = chair_train_lbl / f"{img_file.stem}.txt"
            if lbl_file.exists():
                with open(lbl_file, 'r') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    parts = line.split()
                    if parts:
                        # Offset class index (0 -> 10)
                        parts[0] = str(int(parts[0]) + 10)
                        new_lines.append(" ".join(parts) + "\n")
                
                with open(merged_path / target_split / 'labels' / f"{Path(new_img_name).stem}.txt", 'w') as f:
                    f.writelines(new_lines)

    # 3. Create YAML configuration
    yaml_content = f"""
train: {merged_path.as_posix()}/train/images
val: {merged_path.as_posix()}/valid/images
test: {merged_path.as_posix()}/test/images

nc: 11
names: ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle', 'Chair']
"""
    
    with open(base_path / "data" / "merged_data.yaml", 'w') as f:
        f.write(yaml_content)

    print(f"Merge complete! Merged dataset created at {merged_path}")
    print(f"New configuration saved to data/merged_data.yaml")

if __name__ == "__main__":
    merge_datasets()
