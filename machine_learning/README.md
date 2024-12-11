# Insightku Model - Machine Learning

1. Clone the repository
```
git clone https://github.com/DirzyAdam/Insightku-FinancialApp.git
```

## Model 1 - Forecast Expense

### Overview
The Forecast Expense project leverages machine learning techniques to predict monthly expenses based on historical financial data. By using advanced deep learning architectures like Bidirectional LSTM, this project provides accurate forecasting insights to assist users in better financial planning and budgeting.

### Features
1. Expense Forecasting: Predict future expenses for the upcoming month based on historical spending patterns.
2. Deep Learning Models: Utilizes Bidirectional LSTM architectures for feature extraction and temporal analysis.
3. Customizable Input: Users can tailor forecasting based on their unique dataset.
4. Real-time Updates: Model updates in real-time to reflect changing financial trends.

### How to Use
1. Install dependencies
```
cd Insightku-FinancialApp/machine_learning/Forecast Expense/
pip install requirements.txt
```

#### Test Prediction on Local Computer
1. Run the Flask app
```
py app.py
```
2. Run the prediction with dummy data
```
py prediksi.py
```

## Model 2 - Object Detection + OCR

### Overview
This project combines Object Detection and Optical Character Recognition (OCR) to analyze receipt and extract meaningful information, such as total or amount

### Features
1. Object Detection: Identifies regions of interest (e.g., bounding boxes around items or totals in a document).
2. OCR (Optical Character Recognition): Recognizes and extracts text from identified regions.
3. Data Parsing: Processes extracted text to produce structured outputs (e.g., JSON format).
4. Integration: Combines object detection and OCR for seamless receipt processing

### How to Use
1. Install dependencies
```
cd Insightku-FinancialApp/machine_learning/OCR/
# Ensure you already installed pytesseract
pip install requirements.txt
```

#### Test Object Detection + OCR
```
# run test.ipynb
# model_path = "change/to/your/saved_model/folder/path/"
# image_path = "change/to/your/image/path/"
```

## Acknowledgments
The project utilizes TensorFlow for deep learning.
Special thanks to all contributors and the open-source community for their support.