from ultralytics import YOLO

def train_merged_model():
    # Load the existing best model
    model = YOLO('models/best.pt')
    
    print("Starting training on merged dataset...")
    
    # Train the model
    # We'll use a relatively small number of epochs for fine-tuning
    # but the user can increase this if needed.
    # imgsz=640 is standard for YOLOv8n
    results = model.train(
        data='data/merged_data.yaml',
        epochs=10,  # Small number of epochs for quick demonstration/fine-tuning
        imgsz=640,
        batch=16,
        name='ppe_chair_refined'
    )
    
    print("Training complete!")
    print(f"Results saved to {results.save_dir}")
    print("You can find the new model weights (best.pt) in that directory.")

if __name__ == "__main__":
    train_merged_model()
