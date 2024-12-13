from flask import Flask, request, jsonify
from pipeline import process_image
from database import (
    save_to_database,
    retrieve_records_from_database,
    retrieve_record_by_id,
    update_record_by_id,
    delete_record_by_id,
)
import traceback

app = Flask(__name__)


@app.route("/status", methods=["GET"])
def status():
    """
    Endpoint to check if the server is running.

    Returns:
        JSON response indicating the server status.
    """
    return jsonify({"status": "Server is running"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint to handle image prediction requests.

    Receives an image file, processes it through the OCR pipeline,
    and saves the results to the database.

    Returns:
        JSON response containing the extracted text and other information,
        or an error message if something goes wrong.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]

    try:
        # Process the image using the pipeline
        result = process_image(image_file)

        if result:
            # Save the results to the database
            save_to_database(result, image_file.filename)

            # Return the results
            return jsonify(result), 200
        else:
            return jsonify({"error": "Failed to process image"}), 500

    except Exception as e:
        # Log the error for debugging
        print("Error: ", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/records", methods=["GET"])
def get_records():
    """
    Endpoint to retrieve all OCR processed records.

    Returns:
        JSON response containing the processed records.
    """
    try:
        records = retrieve_records_from_database()
        return jsonify(records), 200
    except Exception as e:
        print("Error: ", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/records/<record_id>", methods=["GET"])
def get_record(record_id):
    """
    Endpoint to retrieve a specific OCR processed record by ID.

    Args:
        record_id: The ID of the record to retrieve.

    Returns:
        JSON response containing the record details.
    """
    try:
        record = retrieve_record_by_id(record_id)
        if record:
            return jsonify(record), 200
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        print("Error: ", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/records/<record_id>", methods=["DELETE"])
def delete_record(record_id):
    """
    Endpoint to delete a specific OCR processed record by ID.

    Args:
        record_id: The ID of the record to delete.

    Returns:
        JSON response indicating whether the deletion was successful.
    """
    try:
        delete_successful = delete_record_by_id(record_id)
        if delete_successful:
            return jsonify({"message": f"Record {record_id} deleted"}), 200
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        print("Error: ", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/records/<record_id>", methods=["PUT"])
def update_record(record_id):
    """
    Endpoint to update a specific OCR processed record by ID.

    Args:
        record_id: The ID of the record to update.
        data: JSON data containing the updated record details.

    Returns:
        JSON response indicating whether the update was successful.
    """
    data = request.json
    try:
        update_successful = update_record_by_id(record_id, data)
        if update_successful:
            return jsonify({"message": f"Record {record_id} updated"}), 200
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        print("Error: ", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/records/<record_id>/amount_paid", methods=["GET", "PUT", "DELETE"])
def manage_amount_paid(record_id):
    """
    Endpoint to view, edit, and delete the 'amount_paid' field of a specific record.

    Args:
        record_id: The ID of the record to manage.

    Returns:
        JSON response indicating the result of the operation.
    """
    try:
        if request.method == "GET":
            record = retrieve_record_by_id(record_id)
            if record:
                return jsonify({"amount_paid": record.get("amount_paid")}), 200
            else:
                return jsonify({"error": "Record not found"}), 404
        elif request.method == "PUT":
            data = request.json
            amount_paid = data.get("amount_paid")
            update_successful = update_record_by_id(
                record_id, {"amount_paid": amount_paid}
            )
            if update_successful:
                return (
                    jsonify({"message": f"Amount paid for record {record_id} updated"}),
                    200,
                )
            else:
                return jsonify({"error": "Record not found"}), 404
        elif request.method == "DELETE":
            update_successful = update_record_by_id(record_id, {"amount_paid": None})
            if update_successful:
                return (
                    jsonify({"message": f"Amount paid for record {record_id} deleted"}),
                    200,
                )
            else:
                return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        print("Error: ", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/records/<record_id>/change_amount", methods=["GET", "PUT", "DELETE"])
def manage_change_amount(record_id):
    """
    Endpoint to view, edit, and delete the 'change_amount' field of a specific record.

    Args:
        record_id: The ID of the record to manage.

    Returns:
        JSON response indicating the result of the operation.
    """
    try:
        if request.method == "GET":
            record = retrieve_record_by_id(record_id)
            if record:
                return jsonify({"change_amount": record.get("change_amount")}), 200
            else:
                return jsonify({"error": "Record not found"}), 404
        elif request.method == "PUT":
            data = request.json
            change_amount = data.get("change_amount")
            update_successful = update_record_by_id(
                record_id, {"change_amount": change_amount}
            )
            if update_successful:
                return (
                    jsonify(
                        {"message": f"Change amount for record {record_id} updated"}
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Record not found"}), 404
        elif request.method == "DELETE":
            update_successful = update_record_by_id(record_id, {"change_amount": None})
            if update_successful:
                return (
                    jsonify(
                        {"message": f"Change amount for record {record_id} deleted"}
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        print("Error: ", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/records/<record_id>/total_price", methods=["GET", "PUT", "DELETE"])
def manage_total_price(record_id):
    """
    Endpoint to view, edit, and delete the 'total_price' field of a specific record.

    Args:
        record_id: The ID of the record to manage.

    Returns:
        JSON response indicating the result of the operation.
    """
    try:
        if request.method == "GET":
            record = retrieve_record_by_id(record_id)
            if record:
                return jsonify({"total_price": record.get("total_price")}), 200
            else:
                return jsonify({"error": "Record not found"}), 404
        elif request.method == "PUT":
            data = request.json
            total_price = data.get("total_price")
            update_successful = update_record_by_id(
                record_id, {"total_price": total_price}
            )
            if update_successful:
                return (
                    jsonify({"message": f"Total price for record {record_id} updated"}),
                    200,
                )
            else:
                return jsonify({"error": "Record not found"}), 404
        elif request.method == "DELETE":
            update_successful = update_record_by_id(record_id, {"total_price": None})
            if update_successful:
                return (
                    jsonify({"message": f"Total price for record {record_id} deleted"}),
                    200,
                )
            else:
                return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        print("Error: ", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Set debug to False in production for security reasons
    app.run(debug=True, host="0.0.0.0")