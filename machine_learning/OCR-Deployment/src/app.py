from flask import Flask, request, jsonify
from pipeline import process_image
from database import save_to_database

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to handle image prediction requests.

    Receives an image file, processes it through the OCR pipeline,
    and saves the results to the database.

    Returns:
        JSON response containing the extracted text and other information,
        or an error message if something goes wrong.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    try:
        # Process the image using the pipeline
        result = process_image(image_file)

        if result:
            # Save the results to the database
            save_to_database(result, image_file.filename)

            # Return the results
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Failed to process image'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
