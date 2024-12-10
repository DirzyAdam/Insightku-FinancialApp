import cv2
import pytesseract
import requests
import numpy as np
import json
import re
from skimage.filters import threshold_local

# TensorFlow Serving configuration (replace with the correct address)
TF_SERVING_URL = 'http://10.0.0.2:8501/v1/models/receiptDetection_model:predict' 

def process_image(image_file):
    """
    Processes the image and performs OCR.

    Args:
        image_file: The image file to be processed.

    Returns:
        The OCR result as a string.
    """

    try:
        # Read the image
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # --- Preprocessing ---

        # 1. Grayscale conversion
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Thresholding
        bw_image = bw_scanner(image)

        # 3. Perspective transform
        receipt_contour = find_receipt_contour(image)
        if receipt_contour is not None:
            bw_image = wrap_perspective(bw_image, receipt_contour.reshape(4, 2))

        # --- Object Detection ---

        # Convert the image to the format expected by TensorFlow Serving
        _, img_encoded = cv2.imencode('.jpg', image)
        data = json.dumps({"signature_name": "serving_default", "instances": [img_encoded.tolist()]})
        headers = {"content-type": "application/json"}

        # Send the image to TensorFlow Serving
        response = requests.post(TF_SERVING_URL, data=data, headers=headers)
        response.raise_for_status()

        # Process the response from TensorFlow Serving
        predictions = response.json()['predictions'][0]

        # Extract bounding boxes from the prediction results
        extracted_text = ""
        for i in range(len(predictions['detection_boxes'])):
            ymin, xmin, ymax, xmax = predictions['detection_boxes'][i]
            (left, right, top, bottom) = (xmin * image.shape[1], xmax * image.shape[1],
                                          ymin * image.shape[0], ymax * image.shape[0])

            # Crop the image based on the bounding box
            cropped_image = bw_image[int(top):int(bottom), int(left):int(right)]

            # Perform OCR using Tesseract on the cropped image
            extracted_text += pytesseract.image_to_string(cropped_image) + " "

        # --- Post-processing ---

        # Clean the text
        extracted_text = extracted_text.replace("\n", " ").strip()
        extracted_text = re.sub(r"[^a-zA-Z0-9\s]", "", extracted_text)

        # Extract the total price
        total_patterns = [
            r'(?:TOTAL|Total|JUMLAH|Jumlah|AMOUNT|Amount)\s*[:]*[Rp$]*\s*([\d.,]+)',
            r'(?:BAYAR|Pay|PAY)[\s:]*[Rp$]*\s*([\d.,]+)',
            r'(?:GRAND\s*TOTAL|Grand Total)[\s:]*[Rp$]*\s*([\d.,]+)',
        ]

        total_price = None
        for pattern in total_patterns:
            match = re.search(pattern, extracted_text, re.IGNORECASE)
            if match:
                total_price = match.group(1)
                total_price = total_price.replace(",", "").replace(".", "")  # Clean thousand and decimal separators
                total_price = float(total_price)
                break

        # Extract the amount paid
        amount_paid_match = re.findall(r"Tunai\s*:\s*\$(\d+\.\d+)", extracted_text)  # Adjust regex to your receipt text
        if amount_paid_match:
            amount_paid = float(amount_paid_match[0])
        else:
            amount_paid = None

        # Extract the change
        change_match = re.findall(r"Kembali\s*:\s*\$(\d+\.\d+)", extracted_text)  # Adjust regex to your receipt text
        if change_match:
            change = float(change_match[0])
        else:
            change = None

        # Return the OCR result and extracted information
        return jsonify({
            'extracted_text': extracted_text, 
            'total_price': total_price,
            'amount_paid': amount_paid,
            'change': change
        }), 200

    except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError) as e:
        return jsonify({'error': f'Error processing image: {e}'}), 500

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

def bw_scanner(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset=5, method="gaussian")
    return (gray > T).astype("uint8") * 255

def wrap_perspective(img, rect):
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))

def find_receipt_contour(image):
    """
    Finds the contour of the receipt in the image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return approx

    return None