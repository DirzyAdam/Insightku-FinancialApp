# Use the TensorFlow Serving base image
FROM tensorflow/serving

# Install dependencies
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx \
                       libglib2.0-0 

# Copy the SavedModel
COPY model/saved_model /models/receipt-detection/1

# Copy model configuration
COPY model_config.conf /models/model_config.conf

# Set the model base path environment variable
ENV MODEL_BASE_PATH=/models/receipt-detection
ENV MODEL_NAME=receiptDetection

# Expose the TensorFlow Serving ports
EXPOSE 8501 8502

# Start TensorFlow Serving
ENTRYPOINT ["tensorflow_model_server", "--port=8501", "--rest_api_port=8502", "--model_config_file=/models/model_config.conf"]