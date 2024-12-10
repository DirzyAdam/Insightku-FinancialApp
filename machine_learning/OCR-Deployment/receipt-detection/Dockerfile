# Use the TensorFlow Serving base image
FROM tensorflow/serving:2.11.0  

# Install dependencies
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx \
                        libglib2.0-0 

# Copy the SavedModel
COPY model/saved_model/1 /models/receiptDetection_model/1

# Copy model configuration
COPY model_config.conf /models/model_config.conf

# Expose port for TensorFlow Serving
EXPOSE 8501