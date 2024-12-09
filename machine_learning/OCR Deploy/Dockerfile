FROM tensorflow/serving:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev \
                        python3-pip

RUN pip install --no-cache-dir opencv-python pytesseract \
                                    flask mysql-connector-python \
                                    tensorflow-object-detection-api

# Copy the trained model
COPY model /models/ocr_model/

# Copy the pipeline script
COPY pipeline.py /app/

# Copy the API script
COPY app.py /app/

# Set the working directory
WORKDIR /app

# Expose ports
EXPOSE 8501  # For TensorFlow Serving
EXPOSE 5000  # For Flask API

# Entrypoint
ENTRYPOINT ["python", "app.py"]  # Replace with the command to run your application