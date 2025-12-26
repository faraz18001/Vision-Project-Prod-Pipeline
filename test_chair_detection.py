import os
import cv2
from ultralytics import YOLO

def test_chair_detection(model_path='models/best.pt', dataset_path='chair-dataset/train/images', num_samples=10):
    # Load the trained YOLOv8 model
    try:
        model = YOLO(model_path)
        print(f"Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Check if dataset directory exists
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset path {dataset_path} does not exist.")
        return

    # Get a list of image files
    #image_files = [f for f in os.listdir(dataset_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]


    image_files=["chair-dataset/train/images/newchairs.png"]
    
    if not image_files:
        print("No images found in the dataset directory.")
        return

    # Limit to num_samples
    samples = image_files[:num_samples]
    
    output_dir = 'output_detections'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nTesting detection on {len(samples)} images from {dataset_path}...\n")
    print(f"{'Image Name':<60} | {'Chair Detected':<15} | {'Confidence':<10} | {'Saved To':<20}")
    print("-" * 120)

    chair_class_id = 10 # Based on merged_data.yaml: ['Hardhat', 'Mask', ..., 'Chair']

    for img_name in samples:
        # Check if img_name is already a path or just a filename
        if os.path.dirname(img_name):
            img_path = img_name
        else:
            img_path = os.path.join(dataset_path, img_name)
        
        # Run inference
        results = model(img_path, verbose=False)
        
        found_chair = False
        max_conf = 0.0
        
        for result in results:
            # Check for chairs
            for box in result.boxes:
                if int(box.cls[0]) == chair_class_id:
                    found_chair = True
                    conf = float(box.conf[0])
                    if conf > max_conf:
                        max_conf = conf
            
            # Save annotated image
            annotated_img = result.plot()
            # Use basename of img_path to avoid subfolders in the filename
            base_filename = os.path.basename(img_path)
            save_path = os.path.join(output_dir, f"annotated_{base_filename}")
            cv2.imwrite(save_path, annotated_img)
        
        status = "Yes" if found_chair else "No"
        conf_str = f"{max_conf:.2f}" if found_chair else "N/A"
        save_status = f"annotated_{os.path.basename(img_path)}"
        
        print(f"{os.path.basename(img_path):<60} | {status:<15} | {conf_str:<10} | {save_status:<20}")

    print(f"\nDetection test complete! Annotated images saved in {output_dir}/")

if __name__ == "__main__":
    test_chair_detection()
