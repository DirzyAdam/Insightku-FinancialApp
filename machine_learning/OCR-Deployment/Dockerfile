# Use a specific version of TensorFlow Serving
FROM tensorflow/serving:2.11.0

# Install dependencies for building Python
RUN apt-get update && \
    apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
                        libnss3-dev libssl-dev libreadline-dev libffi-dev wget \
                        tesseract-ocr libtesseract-dev

# Download Python 3.9 source code
RUN wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz 

# Extract the archive
RUN tar xzf Python-3.9.18.tgz

# Configure and build Python
WORKDIR Python-3.9.18
RUN ./configure --enable-optimizations
RUN make -j $(nproc)
RUN make altinstall

# Clean up
WORKDIR /
RUN rm Python-3.9.18.tgz
RUN rm -rf Python-3.9.18

# Update alternatives for python3 and pip
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.9 1

# Create and activate a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Python libraries from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the trained model
COPY model/saved_model /models/ocr_model/

# Copy the pipeline script
COPY src/pipeline.py /app/

# Copy the API script
COPY src/app.py /app/

# Set the working directory
WORKDIR /app

# Expose ports #1.For TensorFlow Serving # 2.For Flask API
EXPOSE 8501
EXPOSE 5000

# Entrypoint
ENTRYPOINT ["python", "app.py"]