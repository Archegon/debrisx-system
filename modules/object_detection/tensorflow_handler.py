import cv2
import numpy as np
import io
import time
import tflite_runtime.interpreter as tflite
from picamera2 import Picamera2

MODEL_PATH = "/home/debrisx/debrisx-system/models/1.tflite"
LABEL_PATH = "/home/debrisx/debrisx-system/models/coco-labels-2014_2017.txt"

def take_still_image():
    camera = Picamera2()
    camera_config = camera.create_still_configuration()
    camera_config["main"]["size"] = (640, 480)

    camera.configure(camera_config)
    camera.start()

    try:
        time.sleep(2)  # Allow camera to adjust to lighting conditions
        stream = io.BytesIO()
        camera.capture_file(stream, format='jpeg')
        stream.seek(0)
        frame = stream.read()
        return frame
    finally:
        camera.stop()

def load_labels(filename):
    with open(filename, 'r') as file:
        labels = [line.strip() for line in file.readlines()]
    return labels

def load_tflite_model(model_path):
    # Load TFLite model and allocate tensors
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def preprocess_image(frame, input_size):
    frame = cv2.resize(frame, input_size)
    frame = frame.astype(np.float32) / 255.0
    frame = np.expand_dims(frame, axis=0)  # Add batch dimension.
    return frame

def detect_objects(frame, model_path):
    interpreter = load_tflite_model(model_path)
    labels = load_labels(LABEL_PATH)

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    height, width = frame.shape[:2]
    input_data = preprocess_image(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])[0]  # Remove batch dimension

    detections = []
    for detection in output_data:
        x, y, w, h, conf = detection[:5]
        class_probs = detection[5:]
        class_id = np.argmax(class_probs)
        class_score = class_probs[class_id]

        if conf * class_score > 0.5:  # Threshold can be adjusted
            label = labels[class_id]
            x_center = x * width
            y_center = y * height
            box_width = w * width
            box_height = h * height

            x_min = int(x_center - (box_width / 2))
            y_min = int(y_center - (box_height / 2))
            x_max = int(x_center + (box_width / 2))
            y_max = int(y_center + (box_height / 2))

            detections.append((label, class_id, conf * class_score, (x_min, y_min, x_max - x_min, y_max - y_min)))

    return detections

def apply_nms(detections):
    boxes = [det[3] for det in detections]  # Extract bounding boxes
    scores = [det[2] for det in detections]  # Extract scores

    # Convert lists to numpy arrays for OpenCV
    boxes = np.array(boxes)
    scores = np.array(scores)

    # Apply Non-Maximum Suppression
    indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), 0.5, 0.4)

    # Properly check if indices is not empty and handle the data
    if indices is not None and len(indices) > 0:
        # Flatten the array to handle both single and multiple results correctly
        indices = np.array(indices).flatten()
    else:
        return []  # Return an empty list if no indices or indices are empty

    # Filter detections based on NMS indices
    filtered_detections = [detections[i] for i in indices]
    return filtered_detections

def process_and_save_image():
    # Capture an image
    jpeg_bytes = take_still_image()
    
    # Convert JPEG bytes to an OpenCV image
    image = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    model = MODEL_PATH  # Replace with your model
    
    # Detect objects in the image
    detections = detect_objects(image, model)
    filtered_detections = apply_nms(detections)
    
    # Draw bounding boxes on the image
    for label, _, score, (x, y, w, h) in filtered_detections:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        label_text = f"{label}: {score:.2f}"
        cv2.putText(image, label_text, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Save the output image
    cv2.imwrite('detected.jpg', image)

def process_image(image): 
    model = MODEL_PATH  # Replace with your model
    
    # Detect objects in the image
    detections = detect_objects(image, model)
    filtered_detections = apply_nms(detections)
    
    # Draw bounding boxes on the image
    for label, _, score, (x, y, w, h) in filtered_detections:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 1)
        label_text = f"{label}: {score:.2f}"
        cv2.putText(image, label_text, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    return image
