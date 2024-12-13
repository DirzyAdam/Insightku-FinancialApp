import mysql.connector
from config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME

# Database configuration
mydb = mysql.connector.connect(
    host=DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    database=DATABASE_NAME
)
cursor = mydb.cursor(dictionary=True)  # Use dictionary cursor

def save_to_database(result, image_name):
    """
    Saves the OCR results to the database.

    Args:
        result: A dictionary containing the extracted text and other information.
        image_name: The name of the image file.
    """
    try:
        # Validate data (add your validation logic here)
        if not all(key in result for key in ('extracted_text', 'total_price', 'amount_paid', 'change')):
            raise ValueError("Missing required fields in result")

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
    except ValueError as e:
        print(f"Error: {e}")


def retrieve_records_from_database(limit=None, offset=None, order_by=None):
    """
    Retrieves OCR processed records from the database.

    Args:
        limit: Maximum number of records to retrieve.
        offset: Offset for pagination.
        order_by: Column to order by.

    Returns:
        A list of dictionaries containing the records.
    """
    try:
        sql = "SELECT * FROM prediction_results"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"
        if offset:
            sql += f" OFFSET {offset}"
        cursor.execute(sql)
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as err:
        print(f"Error retrieving records: {err}")
        return []


def retrieve_record_by_id(record_id):
    """
    Retrieves a specific OCR processed record by ID from the database.

    Args:
        record_id: The ID of the record to retrieve.

    Returns:
        A dictionary containing the record details if found, otherwise None.
    """
    try:
        sql = "SELECT * FROM prediction_results WHERE id = %s"
        cursor.execute(sql, (record_id,))
        record = cursor.fetchone()
        if record is None:
            print(f"Record with ID {record_id} not found.")
        return record
    except mysql.connector.Error as err:
        print(f"Error retrieving record by ID: {err}")
        return None


def update_record_by_id(record_id, data):
    """
    Updates a specific OCR processed record by ID in the database.

    Args:
        record_id: The ID of the record to update.
        data: A dictionary containing the updated record details.

    Returns:
        True if the update was successful, otherwise False.
    """
    try:
        # Validate data (add your validation logic here)
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")

        fields = ", ".join(f"{key} = %s" for key in data)
        values = list(data.values())
        values.append(record_id)
        sql = f"UPDATE prediction_results SET {fields} WHERE id = %s"
        cursor.execute(sql, values)
        mydb.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Error updating record: {err}")
        return False
    except ValueError as e:
        print(f"Error: {e}")
        return False


def delete_record_by_id(record_id):
    """
    Deletes a specific OCR processed record by ID from the database.

    Args:
        record_id: The ID of the record to delete.

    Returns:
        True if the deletion was successful, otherwise False.
    """
    try:
        # Add confirmation before deleting (optional)
        confirmation = input(f"Are you sure you want to delete record {record_id}? (y/n): ")
        if confirmation.lower() != 'y':
            return False

        sql = "DELETE FROM prediction_results WHERE id = %s"
        cursor.execute(sql, (record_id,))
        mydb.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Error deleting record: {err}")
        return False