FROM tensorflow/serving:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev \
                        python3-pip

# Install Python libraries from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the trained model (path yang benar)
COPY model/saved_model /models/ocr_model/ 

# Copy the pipeline script
COPY src/pipeline.py /app/

# Copy the API script
COPY src/app.py /app/

# Set the working directory
WORKDIR /app

# Expose ports
EXPOSE 8501  # For TensorFlow Serving
EXPOSE 5000  # For Flask API

# Entrypoint
ENTRYPOINT ["python", "app.py"]