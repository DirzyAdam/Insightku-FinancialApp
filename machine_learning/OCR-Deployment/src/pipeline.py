from preprocessing import preprocess_image
from object_detection import detect_objects
from ocr import perform_ocr
from postprocessing import extract_information

def process_image(image_file):
    """
    Processes an image through the OCR pipeline.

    Performs preprocessing, object detection, OCR, and post-processing
    on the given image file.

    Args:
        image_file: The image file to be processed.

    Returns:
        A dictionary containing the extracted text and other information,
        or None if an error occurs.
    """
    try:
        # Preprocessing
        preprocessed_image = preprocess_image(image_file)

        # Object Detection
        detection_results = detect_objects(preprocessed_image)

        # OCR
        extracted_text = perform_ocr(preprocessed_image, detection_results)

        # Post-processing
        extracted_info = extract_information(extracted_text)

        return {
            'extracted_text': extracted_text,
            **extracted_info
        }

    except Exception as e:
        print(f'Error processing image: {e}')
        return None