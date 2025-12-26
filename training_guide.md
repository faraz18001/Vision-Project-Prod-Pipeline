# Model Training Guide

This guide explains how to train the detection model using Google Colab and Kaggle.

## Option 1: Google Colab

Follow these steps to train using Google Colab.

1. **Upload Files**: Upload the project folder to your Google Drive.
2. **Open Notebook**: Open `colab_training.ipynb` in Google Colab.
3. **Connect to GPU**: Go to Edit > Notebook settings and select 'T4 GPU' as the Hardware accelerator.
4. **Run Step 1 (Mount Drive)**: Run the first cell and follow the link to give access to your Google Drive.
5. **Run Step 2 (Navigate)**: Run the second cell to move into the project folder. Ensure the path matches your folder name in Drive.
6. **Run Step 3 (Install)**: Run the cell to install the necessary software.
7. **Run Step 4 (Update Paths)**: Run the cell to update the configuration file with the current paths.
8. **Run Step 5 (Train)**: Run the final cell to start the training. The process will take some time.

## Option 2: Kaggle

Follow these steps to train using Kaggle.

1. **Create Notebook**: Create a new notebook on Kaggle.
2. **Add Data**: Click 'Add Data' and upload your project folder or dataset as a private dataset.
3. **Turn on GPU**: In the 'Settings' pane on the right, set Accelerator to 'GPU P100' or 'GPU T4 x2'.
4. **Locate Data**: Use the first cell in `kaggle-training.ipynb` to find where your data is stored on Kaggle.
5. **Install Software**: Run the cell that installs 'ultralytics'.
6. **Setup Configuration**: Run the cell that creates the `merged_data.yaml` file. This tells the system where the images are located.
7. **Start Training**: Run the training cell. The results and the trained model will be saved in the `/kaggle/working/runs` folder.

## How to Get Results

Once training finishes, look for a file named `best.pt`. 
- In Colab, it will be in the `runs/ppe_chair_colab/weights/` folder.
- In Kaggle, it will be in the `/kaggle/working/runs/ppe_detection/weights/` folder.
