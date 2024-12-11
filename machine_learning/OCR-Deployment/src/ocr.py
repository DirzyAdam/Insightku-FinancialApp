import pytesseract

def perform_ocr(image, detection_results):
    """
    Performs OCR on the detected objects in the image.
    Args:
        image: The image to perform OCR on.
        detection_results: The object detection results containing bounding boxes.
    Returns:
        The extracted text as a string.
    """
    extracted_text = ""
    for i in range(len(detection_results['detection_boxes'])):
        ymin, xmin, ymax, xmax = detection_results['detection_boxes'][i]
        (left, right, top, bottom) = (xmin * image.shape[1], xmax * image.shape[1],
                                      ymin * image.shape[0], ymax * image.shape[0])
        cropped_image = image[int(top):int(bottom), int(left):int(right)]
        config = '--psm 6 --oem 3'
        extracted_text += pytesseract.image_to_string(cropped_image, config=config) + " "
    return extracted_text
