import cv2
import pytesseract
import requests
import numpy as np
import json

# TensorFlow Serving configuration
TF_SERVING_URL = 'http://localhost:8501/v1/models/ocr_model:predict'  # Replace with the correct address and port

def process_image(image_file):
    """
    Processes the image and performs OCR.

    Args:
        image_file: The image file to be processed.

    Returns:
        The OCR result as a string.
    """

    # Read the image
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Convert the image to the format expected by TensorFlow Serving
    _, img_encoded = cv2.imencode('.jpg', image)
    data = json.dumps({"signature_name": "serving_default", "instances": [img_encoded.tolist()]})
    headers = {"content-type": "application/json"}

    # Send the image to TensorFlow Serving
    response = requests.post(TF_SERVING_URL, data=data, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Process the response from TensorFlow Serving
    try:
        predictions = response.json()['predictions'][0]
    except (KeyError, json.JSONDecodeError) as e:
        raise ValueError("Invalid response from TensorFlow Serving") from e

    # Extract bounding boxes from the prediction results
    extracted_text = ""
    for i in range(len(predictions['detection_boxes'])):
        ymin, xmin, ymax, xmax = predictions['detection_boxes'][i]
        (left, right, top, bottom) = (xmin * image.shape[1], xmax * image.shape[1],
                                      ymin * image.shape[0], ymax * image.shape[0])

        # Crop the image based on the bounding box
        cropped_image = image[int(top):int(bottom), int(left):int(right)]

        # Perform OCR using Tesseract on the cropped image
        extracted_text += pytesseract.image_to_string(cropped_image) + " "

    # (Optional) Post-processing
    # ...

    return extracted_text