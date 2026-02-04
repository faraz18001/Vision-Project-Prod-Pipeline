# YOLOv8 Object Detection - Iterative Training Framework

A flexible object detection project built on YOLOv8 that allows you to **retrain and refine** the model to detect new objects over time.

![Detection Demo](assets/videoconstruc2.gif)

## About This Project

This project started as a PPE (Personal Protective Equipment) detection model for construction sites. The key feature is the **iterative training workflow** - you can keep refining the model to detect new classes without starting from scratch.

For example, the original model detected:
- Hardhat, Mask, Safety Vest, Safety Cone, Person, Machinery, Vehicle

After refinement training, I added:
- **Chair detection** - by collecting new data and retraining using the notebooks in this repo

This makes the model adaptable for different use cases where you need to add new detection classes over time.

## Project Structure

```
├── models/
│   ├── best.pt          # Original trained model
│   ├── refined.pt       # Refined model with new classes
│   └── yolov8n.pt       # Base YOLOv8 nano model
├── notebooks/
│   ├── colab_training.ipynb    # Training on Google Colab
│   └── kaggle-training.ipynb   # Training on Kaggle
├── results/             # Training metrics and visualizations
├── output/              # Detection output examples
├── source_files/        # Test images and videos
├── assets/              # README images
├── webcam_inference.py  # Real-time webcam detection
├── train_merged.py      # Local training script
├── merge_datasets.py    # Tool to merge multiple datasets
└── training_guide.md    # Step-by-step training instructions
```

## How to Use

### 1. Install Dependencies
```bash
pip install ultralytics opencv-python
```

### 2. Run Webcam Detection
```bash
python webcam_inference.py
```
- Uses the `models/best.pt` model by default
- Press **'q'** to exit

### 3. Retrain with New Classes

To add new detection classes:

1. Collect images of the new object
2. Label them using a tool like Roboflow or LabelImg
3. Use the notebooks in `notebooks/` to retrain:
   - **Google Colab**: `notebooks/colab_training.ipynb`
   - **Kaggle**: `notebooks/kaggle-training.ipynb`

## Current Detection Classes

The refined model can detect:
- Hardhat / NO-Hardhat
- Mask / NO-Mask
- Safety Vest / NO-Safety Vest
- Person
- Safety Cone
- Machinery
- Vehicle
- Chair (added through refinement)

## Training Workflow

1. **Prepare Dataset** - Collect and label images for new classes
2. **Merge Datasets** - Use `merge_datasets.py` to combine with existing data
3. **Train on Cloud** - Use the notebooks for GPU-powered training
4. **Get Model** - Download the new `best.pt` from training output
5. **Test** - Run inference to verify the new detections work

## License

This project uses the YOLOv8 model by Ultralytics. The original PPE detection dataset is from [Roboflow Construction Site Safety Dataset](https://universe.roboflow.com/roboflow-universe-projects/construction-site-safety).

