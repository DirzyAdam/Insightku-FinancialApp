import requests
import json
import cv2
import numpy as np

# TensorFlow Serving URL
TF_SERVING_URL = 'http://10.0.0.4:8502/v1/models/receiptDetection:predict'

def detect_objects(image):
    """
    Detects objects in the image using TensorFlow Serving.
    Sends the image to TensorFlow Serving and returns the prediction results.
    """
    try:
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (1280, 1280))
        img_array = np.expand_dims(img_resized, axis=0)  # Add batch dimension
        img_array = img_array.astype(np.uint8)  # Ensure the data type is uint8

        img_list = img_array.tolist()
        data = json.dumps({
            "signature_name": "serving_default",
            "inputs": {"input_tensor": img_list}
        })
        headers = {"content-type": "application/json"}

        # Send request to TensorFlow Serving
        response = requests.post(TF_SERVING_URL, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        predictions = response.json()
        outputs = predictions['outputs']
        detection_boxes = outputs['detection_boxes'][0]  # Access the first element in the list

        # Ensure the detection boxes are correctly handled
        boxes = []
        for i, box in enumerate(detection_boxes):
            if isinstance(box, list) and len(box) == 4:
                boxes.append(box)

        # Select the largest box
        if boxes:
            largest_box = max(boxes, key=lambda box: (box[2] - box[0]) * (box[3] - box[1]))
            return {'detection_boxes': [largest_box]}
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to TensorFlow Serving: {e}")
        return None
    except (KeyError, json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"Error decoding response from TensorFlow Serving: {e}")
        return None
