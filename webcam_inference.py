import cv2
from ultralytics import YOLO

def run_webcam_inference(model_path='models/best.pt'):
    # Load the trained YOLOv8 model
    try:
        model = YOLO(model_path)
        print(f"Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Open the default webcam (source 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam opened. Press 'q' to exit.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Run YOLOv8 inference on the frame
        # stream=True is more efficient for long-running video
        results = model.predict(source=frame, show=False, conf=0.5)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the resulting frame
        cv2.imshow('PPE Detection - Construction Site Safety', annotated_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_webcam_inference()
