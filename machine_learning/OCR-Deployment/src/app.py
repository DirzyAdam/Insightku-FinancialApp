from flask import Flask, request, jsonify
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import mysql.connector
from pipeline import process_image
from skimage.filters import threshold_local

app = Flask(__name__)

# Cloud SQL configuration
mydb = mysql.connector.connect(
    host="your_db_host",  # Replace with your Cloud SQL host
    user="your_db_user",  # Replace with your Cloud SQL user
    password="your_db_password",  # Replace with your Cloud SQL password
    database="your_db_name"  # Replace with your database name
)
cursor = mydb.cursor()

# --- Preprocessing functions ---

def bw_scanner(image):
    """
    Converts an image to grayscale and applies adaptive thresholding.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset=5, method="gaussian")
    return (gray > T).astype("uint8") * 255

def wrap_perspective(img, rect):
    """
    Applies perspective transform to an image.
    """
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

# -----------------------------------

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    
    try:
        # --- Preprocessing ---
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        
        # 1. Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Apply thresholding
        bw_result = bw_scanner(image)

        # 3. Apply perspective transform
        receipt_contour = find_receipt_contour(image)
        if receipt_contour is not None:
            bw_result = wrap_perspective(bw_result, receipt_contour.reshape(4, 2))
        else:
            return jsonify({'error': 'Receipt contour not found'}), 500  # Error handling if no contour is found

        # --- OCR ---
        d = pytesseract.image_to_data(bw_result, output_type=Output.DICT)
        n_boxes = len(d['level'])
        extracted_text = ""
        for i in range(n_boxes):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            extracted_text += d['text'][i] + " "

        # --- Save to database ---
        try:
            sql = "INSERT INTO prediction_results (user_id, image_name, extracted_text, amounts, merchant_name, transaction_date, confidence_score) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (1, image_file.filename, extracted_text, 0, "unknown", "2024-12-10", 0.8)  # Replace with appropriate values
            cursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as err:
            return jsonify({'error': f'Database error: {err}'}), 500  # Database error handling

        # Return the prediction results
        return jsonify({'extracted_text': extracted_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')