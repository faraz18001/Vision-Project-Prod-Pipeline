"""
Roboflow Auto-Labeling Script
Generates labels AND saves annotated images with bounding boxes.
"""

import os
import shutil
import zipfile
from PIL import Image, ImageDraw, ImageFont
from roboflow import Roboflow

# ============ CONFIGURATION ============
PROJECT_ROOT = r"c:/Users/Tesla Laptops/Videos/Construction-Site-Safety-PPE-Detection"

# Your Roboflow API key
ROBOFLOW_API_KEY = "yodvcrpET4mwCUMKfZ8I"

# Input images folder
INPUT_IMAGES = f"{PROJECT_ROOT}/new_images"

# Output folder
OUTPUT_FOLDER = f"{PROJECT_ROOT}/roboflow_labels"

# =======================================

# Colors for different classes (RGB)
CLASS_COLORS = {
    'Hardhat': (0, 255, 0),        # Green
    'Mask': (0, 200, 255),          # Cyan
    'NO-Hardhat': (255, 0, 0),      # Red
    'NO-Mask': (255, 100, 100),     # Light Red
    'NO-Safety Vest': (255, 50, 50),# Dark Red
    'Person': (255, 255, 0),        # Yellow
    'Safety Cone': (255, 165, 0),   # Orange
    'Safety Vest': (0, 255, 200),   # Teal
    'machinery': (128, 0, 255),     # Purple
    'vehicle': (100, 100, 255),     # Blue
}

# Class names list (for CVAT export)
CLASS_NAMES = [
    'Hardhat',
    'Mask',
    'NO-Hardhat',
    'NO-Mask',
    'NO-Safety Vest',
    'Person',
    'Safety Cone',
    'Safety Vest',
    'machinery',
    'vehicle'
]


def draw_boxes(image_path, predictions, output_path):
    """Draw bounding boxes on image and save."""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    for pred in predictions:
        class_name = pred['class']
        x = pred['x']
        y = pred['y']
        w = pred['width']
        h = pred['height']
        conf = pred['confidence']
        
        # Calculate box coordinates
        x1 = int(x - w/2)
        y1 = int(y - h/2)
        x2 = int(x + w/2)
        y2 = int(y + h/2)
        
        # Get color for this class
        color = CLASS_COLORS.get(class_name, (255, 255, 255))
        
        # Draw box
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        
        # Draw label
        label = f"{class_name} {conf:.2f}"
        draw.rectangle([x1, y1-20, x1+len(label)*8, y1], fill=color)
        draw.text((x1+2, y1-18), label, fill=(0, 0, 0))
    
    img.save(output_path)
    return img


def main():
    print("Roboflow Auto-Labeling Script")
    print("=" * 50)
    
    # Create output folders
    labels_folder = f"{OUTPUT_FOLDER}/labels"
    images_folder = f"{OUTPUT_FOLDER}/annotated_images"
    os.makedirs(labels_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)
    
    # Connect to Roboflow
    print("\nConnecting to Roboflow...")
    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace().project("construction-site-safety")
    model = project.version(25).model
    print("Model loaded!")
    
    # Get image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    for f in os.listdir(INPUT_IMAGES):
        ext = os.path.splitext(f)[1].lower()
        if ext in image_extensions:
            image_files.append(f)
    
    print(f"\nFound {len(image_files)} images to process")
    
    # Process each image
    for i, image_file in enumerate(image_files):
        image_path = os.path.join(INPUT_IMAGES, image_file)
        
        # Get image dimensions
        img = Image.open(image_path)
        img_width = img.width
        img_height = img.height
        
        # Run prediction
        result = model.predict(image_path, confidence=40, overlap=30).json()
        predictions = result['predictions']
        
        # Save YOLO format labels
        label_file = os.path.splitext(image_file)[0] + '.txt'
        label_path = os.path.join(labels_folder, label_file)
        
        with open(label_path, 'w') as f:
            for pred in predictions:
                class_name = pred['class']
                x_center = pred['x'] / img_width
                y_center = pred['y'] / img_height
                width = pred['width'] / img_width
                height = pred['height'] / img_height
                confidence = pred['confidence']
                
                # Get class ID
                if class_name in CLASS_NAMES:
                    class_id = CLASS_NAMES.index(class_name)
                else:
                    class_id = 0
                
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f} {confidence:.6f}\n")
        
        # Save annotated image
        annotated_path = os.path.join(images_folder, image_file)
        draw_boxes(image_path, predictions, annotated_path)
        
        print(f"[{i+1}/{len(image_files)}] {image_file}: {len(predictions)} detections")
    
    print(f"\nLabels saved to: {labels_folder}")
    print(f"Annotated images saved to: {images_folder}")
    
    # Create CVAT package
    print("\nCreating CVAT package...")
    cvat_folder = f"{OUTPUT_FOLDER}/cvat_package"
    if os.path.exists(cvat_folder):
        shutil.rmtree(cvat_folder)
    os.makedirs(cvat_folder)
    
    # Create obj.names
    with open(f"{cvat_folder}/obj.names", 'w') as f:
        for name in CLASS_NAMES:
            f.write(name + '\n')
    
    # Create obj.data
    with open(f"{cvat_folder}/obj.data", 'w') as f:
        f.write(f"classes = {len(CLASS_NAMES)}\n")
        f.write("names = obj.names\n")
    
    # Copy labels
    shutil.copytree(labels_folder, f"{cvat_folder}/labels")
    
    # Create zip
    zip_path = f"{OUTPUT_FOLDER}/cvat_upload.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(cvat_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, cvat_folder)
                zipf.write(file_path, arcname)
    
    print(f"CVAT zip created: {zip_path}")
    print("\nDone!")


if __name__ == "__main__":
    main()
