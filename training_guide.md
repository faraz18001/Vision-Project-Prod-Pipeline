# Re-Training the Model with New PPEs

When you want to add new PPE classes or new images to the model, follow these steps.

## Step 1: Prepare Your Data

1. Add new images to `merged-dataset/train/images/`
2. Add corresponding label files to `merged-dataset/train/labels/`
3. Update `data/merged_data.yaml` with any new class names in the `names` list and update `nc` (number of classes)

## Step 2: Train

### Google Colab

1. Upload project folder to Google Drive
2. Open `notebooks/colab_training.ipynb` in Colab
3. Set GPU: Edit > Notebook settings > T4 GPU
4. Run cells in order:
   - Mount Drive
   - Navigate to project folder
   - Install: `!pip install ultralytics`
   - Update paths
   - Start training
5. Get trained model from `runs/ppe_chair_colab/weights/best.pt`

### Kaggle

1. Create new notebook on Kaggle
2. Upload project as private dataset via "Add Data"
3. Enable GPU in Settings panel
4. Run cells from `notebooks/kaggle-training.ipynb`:
   - Explore dataset structure to find your data path
   - Install: `!pip install ultralytics`
   - Create `merged_data.yaml` with correct paths
   - Start training
5. Get trained model from `/kaggle/working/runs/ppe_detection/weights/best.pt`

## Step 3: Use New Model

Copy `best.pt` to `models/` folder and update your inference code to use it.
