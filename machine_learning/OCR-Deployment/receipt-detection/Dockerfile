# Use the TensorFlow Serving base image; Replace with the appropriate version if needed
FROM tensorflow/serving:2.11.0

# Install dependencies
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx \
                        libglib2.0-0 

# Copy the SavedModel; Adjust the path if different
COPY model/saved_model /models/receiptDetection_model

# Expose port for TensorFlow Serving
EXPOSE 8501