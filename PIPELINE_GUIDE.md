# Production Pipeline Guide

This guide explains how to add new data, annotate it, upload it, and retrain the model.

## 1. Directory Structure

```
/Vision-Project-Prod-Pipeline/
├── 1_raw_footage/          <-- DROP VIDEOS HERE
├── 2_processed_images/     <-- Script puts images here
├── 3_roboflow_upload/      <-- Script puts "ready to upload" folders here
├── 4_training_data/        <-- Unzip Roboflow Export here
├── Pipe-Lines/             
│   ├── Annotation_Pipeline.ipynb
│   └── Training_Pipeline.ipynb
└── models/                 <-- Your 'best.pt' lives here
```

## 2. Step-by-Step Workflow

### Phase A: Add Data & Auto-Label

1. **Drop Video**: Put your new `.mp4` files into `1_raw_footage`.
2. **Extract Frames**:
    Open a terminal and run:

    ```bash
    python extract_frames.py
    ```

    *(This converts videos to images in `2_processed_images`)*
3. **Run Auto-Labeler**:
    Open `Pipe-Lines/Annotation_Pipeline.ipynb` in Colab.
    * **Action**: Run all cells.
    * **Result**: It detects objects, filters for **Hardhat/Person/Vest**, and saves everything to `3_roboflow_upload`.

### Phase B: Upload to Roboflow

1. Go to your Roboflow Project.
2. Click **"Upload Data"**.
3. Drag and drop the **`3_roboflow_upload/images`** and **`3_roboflow_upload/labels`** folders.
4. Roboflow will match them automatically. **Verify** the boxes look correct.
5. Click **"Generate Version"**.
6. Export as **YOLOv8** (ZIP).

### Phase C: Retrain Model

1. **Download**: Get your new ZIP from Roboflow.
2. **Unzip**: Unzipping it into `4_training_data`.
    * *Example path*: `4_training_data/dataset_v2`
3. **Run Training**:
    Open `Pipe-Lines/Training_Pipeline.ipynb` in Colab.
    * **Action**: Run all cells.
    * **Result**: It finds your new folder, loads your old `best.pt`, retrains it, and saves a new `best.pt`.
