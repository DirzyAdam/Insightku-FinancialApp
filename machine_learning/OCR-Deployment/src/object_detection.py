import requests
import json
import cv2
import numpy as np

# TensorFlow Serving URL
TF_SERVING_URL = 'http://34.128.119.224:8502/v1/models/receiptDetection:predict'

def detect_objects(image):
    """
    Detects objects in the image using TensorFlow Serving.
    Sends the image to TensorFlow Serving and returns the prediction results.
    """
    try:
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (640, 640))  # Resize to 640x640 as required by the model
        img_array = np.expand_dims(img_resized, axis=0)  # Add batch dimension
        img_array = img_array.astype(np.uint8)  # Ensure the data type is uint8

        print("Image array shape:", img_array.shape)
        img_list = img_array.tolist()
        data = json.dumps({
            "signature_name": "serving_default",
            "inputs": {"input_tensor": img_list}
        })
        headers = {"content-type": "application/json"}
        print("Request JSON:", data)
        response = requests.post(TF_SERVING_URL, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        predictions = response.json()
        print("Response JSON:", json.dumps(predictions, indent=4))  # Print the entire response
        print("Available keys in response:", predictions.keys())
        outputs = predictions['outputs']
        print("Available keys in outputs:", outputs.keys())
        detection_boxes = outputs['detection_boxes'][0]  # Access the first element in the list
        print("Detection Boxes:", detection_boxes)
        # Collect individual box coordinates into a list
        boxes = []
        for i, box in enumerate(detection_boxes):
            print(f"Box {i}: {box}")
            boxes.append(box)
        # Select the largest box
        largest_box = max(boxes, key=lambda box: (box[2] - box[0]) * (box[3] - box[1]))
        return {'detection_boxes': [largest_box]}
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to TensorFlow Serving: {e}")
        return None
    except (KeyError, json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"Error decoding response from TensorFlow Serving: {e}")
        return None
