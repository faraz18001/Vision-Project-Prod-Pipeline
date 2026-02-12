# Construction Site PPE Detection — YOLOv8

A real-time **PPE (Personal Protective Equipment)** detection system for construction sites, built on YOLOv8. The model detects **Hardhats**, **Persons**, and **Safety Vests** in images and video.

## Demo

![PPE Detection Demo](./ppe_detection_demo.gif)

## Detection Classes

| Class ID | Class | Description |
|---|---|---|
| 0 | **Hardhat** | Safety helmet worn on head |
| 1 | **Person** | Workers on site |
| 2 | **Safety Vest** | High-visibility vest |

## Model Performance

Trained on **2,700 images** (2,500 general PPE + 190 site-specific), fine-tuned YOLOv8 Nano:

| Class | Precision | Recall | mAP50 |
|---|---|---|---|
| Hardhat | 91.9% | 77.2% | 85.6% |
| Person | 89.5% | 72.3% | 82.9% |
| Safety Vest | 100% | 87.6% | 92.5% |
| **Overall** | **93.8%** | **79.0%** | **87.0%** |

## Project Structure

```
├── models/
│   └── best.pt                # Trained YOLOv8n model (3 classes)
├── footage/                   # Input videos
├── annotated_videos/          # Output annotated videos
├── annotated_output/          # Output annotated images
├── data/                      # Dataset config (data.yaml)
├── notebooks/
│   ├── colab_training.ipynb   # Training on Google Colab
│   └── kaggle-training.ipynb  # Training on Kaggle
├── run_video_inference.py     # Video inference + saves annotated video
├── batch_annotate.py          # Batch image annotation
├── images_to_video.py         # Convert image folder to video
├── filter_classes.py          # Filter dataset to specific classes
└── assets/                    # README assets (GIFs, images)
```

## Quick Start

### 1. Install Dependencies
```bash
python -m venv vision
source vision/bin/activate
pip install -r requirements.txt
```

### 2. Run Video Inference
```bash
python run_video_inference.py
```
- Place a video file in `footage/`
- Annotated video is saved to `annotated_videos/`
- Press **'q'** or **ESC** to exit

### 3. Batch Annotate Images
```bash
python batch_annotate.py
```
- Place images in `trained_test/`
- Annotated images are saved to `annotated_output/`

### 4. Convert Images to Video
```bash
python images_to_video.py
```

## Training Workflow

1. **Prepare Dataset** — Collect and label images on [Roboflow](https://roboflow.com) with 3 classes
2. **Filter Classes** — Use `filter_classes.py` to reduce a multi-class dataset to the 3 target classes
3. **Train on Cloud** — Use the notebooks for GPU-powered training (Colab/Kaggle)
4. **Fine-tune** — Retrain with site-specific images using the existing model as base
5. **Test** — Run inference to verify detections

## License

This project uses the YOLOv8 model by [Ultralytics](https://ultralytics.com). The PPE detection dataset is from [Roboflow Construction Site Safety Dataset](https://universe.roboflow.com/roboflow-universe-projects/construction-site-safety).


