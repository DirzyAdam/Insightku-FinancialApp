from flask import Flask, request, jsonify
import mysql.connector
from pipeline import process_image

app = Flask(__name__)

# Cloud SQL configuration
mydb = mysql.connector.connect(
    host="your_db_host",  # Replace with your Cloud SQL host
    user="your_db_user",  # Replace with your Cloud SQL user
    password="your_db_password",  # Replace with your Cloud SQL password
    database="your_db_name"  # Replace with your database name
)
cursor = mydb.cursor()

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    
    try:
        # Process the image using the pipeline
        extracted_text = process_image(image_file)

        # Save the prediction results to Cloud SQL
        sql = "INSERT INTO prediction_results (user_id, image_name, extracted_text, amounts, merchant_name, transaction_date, confidence_score) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (1, image_file.filename, extracted_text, 0, "unknown", "2024-12-10", 0.8)  # Replace with appropriate values
        cursor.execute(sql, val)
        mydb.commit()

        # Return the prediction results
        return jsonify({'extracted_text': extracted_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')