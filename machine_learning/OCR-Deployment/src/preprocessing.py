import cv2
import numpy as np
from skimage.filters import threshold_local

def bw_scanner(image):
    """
    Converts an image to grayscale and applies adaptive thresholding.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 21, offset=5, method="gaussian")
    bw = (gray > T).astype("uint8") * 255
    print("BW Scanner output shape:", bw.shape)
    return bw

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
    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    print("Warped output shape:", warped.shape)
    return warped

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
            print("Found receipt contour:", approx)
            return approx
    return None

def preprocess_image(image_file):
    """
    Preprocesses the image by converting to grayscale, applying
    thresholding, and performing perspective transform if necessary.
    """
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bw_result = bw_scanner(image)
    receipt_contour = find_receipt_contour(image)
    if receipt_contour is not None:
        bw_result = wrap_perspective(bw_result, receipt_contour.reshape(4, 2))
    else:
        print("No receipt contour found.")
    
    # Additional Preprocessing Steps
    bw_result = cv2.medianBlur(bw_result, 3)
    bw_result = cv2.adaptiveThreshold(bw_result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Resize and normalize the image
    bw_result = cv2.resize(bw_result, (1280, 1280))  # Resize to match model input size
    bw_result = bw_result / 255.0
    print("Preprocessed image shape:", bw_result.shape)
    
    # Add a batch dimension and channel dimension
    bw_result = np.expand_dims(bw_result, axis=0)
    bw_result = np.expand_dims(bw_result, axis=-1)  # Adding channel dimension
    print("Final preprocessed image shape with batch and channel dimensions:", bw_result.shape)
    
    # Convert to uint8 to avoid depth error
    bw_result = (bw_result * 255).astype(np.uint8)
    print("Final preprocessed image dtype:", bw_result.dtype)

    return bw_result
