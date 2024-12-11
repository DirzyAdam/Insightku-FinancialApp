import requests
import json
import numpy as np

# TensorFlow Serving URL
TF_SERVING_URL = 'http://localhost:8501/v1/models/receiptDetection:predict' 

def detect_objects(image):
    """
    Detects objects in the image using TensorFlow Serving.

    Sends the image to TensorFlow Serving and returns the prediction results.
    """
    # Convert the image to the format expected by TensorFlow Serving
    _, img_encoded = cv2.imencode('.jpg', image)
    data = json.dumps({"signature_name": "serving_default", "instances": [img_encoded.tolist()]})
    headers = {"content-type": "application/json"}

    # Send the image to TensorFlow Serving
    response = requests.post(TF_SERVING_URL, data=data, headers=headers)
    response.raise_for_status()

    # Process the response
    predictions = response.json()['predictions'][0]
    return predictions