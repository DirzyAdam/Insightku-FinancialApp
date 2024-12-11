import mysql.connector
from config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME

# Database configuration
mydb = mysql.connector.connect(
  host=DATABASE_HOST,
  user=DATABASE_USER,
  password=DATABASE_PASSWORD,
  database=DATABASE_NAME
)
cursor = mydb.cursor()

def save_to_database(result, image_name):
    """
    Saves the OCR results to the database.

    Args:
        result: A dictionary containing the extracted text and other information.
        image_name: The name of the image file.
    """
    try:
        sql = """
        INSERT INTO prediction_results 
        (image_name, extracted_text, total_price, amount_paid, change) 
        VALUES (%s, %s, %s, %s, %s)
        """
        val = (
            image_name, result.get('extracted_text'), 
            result.get('total_price'), result.get('amount_paid'), result.get('change')
        )
        cursor.execute(sql, val)
        mydb.commit()
        print(f"Data saved to database for image: {image_name}")
    except mysql.connector.Error as err:
        print(f"Error saving to database: {err}")
