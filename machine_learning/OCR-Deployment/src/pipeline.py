from preprocessing import preprocess_image
from object_detection import detect_objects
from ocr import perform_ocr
from postprocessing import extract_information
import numpy as np

def process_image(image_file):
    """
    Processes an image through the OCR pipeline.
    """
    try:
        # Preprocessing
        preprocessed_image = preprocess_image(image_file)
        # Convert preprocessed image back to standard format for object detection
        preprocessed_image = preprocessed_image[0, :, :, 0].astype(np.uint8)  # Remove batch and channel dimension

        # Object Detection
        detection_results = detect_objects(preprocessed_image)
        
        if detection_results is None:
            raise ValueError("Object detection failed")

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
