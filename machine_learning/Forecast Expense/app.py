from flask import Flask, request, jsonify
import tensorflow as tf
import pandas as pd
import numpy as np
import json
import joblib
from datetime import timedelta

app = Flask(__name__)

def load_forecasting_model():
    try:
        # Load model
        loaded_model = tf.keras.models.load_model('expense_forecast_model.h5')
        
        # Load parameter
        with open('model_params.json', 'r') as f:
            params = json.load(f)
        
        # Load scaler
        loaded_scaler = joblib.load('scaler.pkl')
        
        # Load encoders
        encoder_mode = joblib.load('encoder_mode.pkl')
        encoder_category = joblib.load('encoder_category.pkl')
        encoder_subcategory = joblib.load('encoder_subcategory.pkl')
        
        # Load encoder column names
        encoder_columns = joblib.load('encoder_columns.pkl')
        
        return {
            'model': loaded_model,
            'params': params,
            'scaler': loaded_scaler,
            'encoder_mode': encoder_mode,
            'encoder_category': encoder_category,
            'encoder_subcategory': encoder_subcategory,
            'mode_columns': encoder_columns['mode_columns'],
            'category_columns': encoder_columns['category_columns'],
            'subcategory_columns': encoder_columns['subcategory_columns']
        }
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
    
def prepare_new_data(input_data, model_components):
    try:
        required_columns = ['Date']
        missing_cols = [col for col in required_columns if col not in input_data.columns]
        if missing_cols:
            raise ValueError(f"Input data is missing the following columns: {missing_cols}")

        # Konversi datetime
        input_data['Date'] = pd.to_datetime(input_data['Date'])
        
        # Ekstraksi fitur waktu
        input_data['year'] = input_data['Date'].dt.year
        input_data['month'] = input_data['Date'].dt.month
        input_data['day'] = input_data['Date'].dt.day
        input_data['dayofweek'] = input_data['Date'].dt.dayofweek
        
        # Drop kolom yang tidak diperlukan
        input_data_processed = input_data.drop(columns=['Note', 'Currency', 'Date'])
        
        # One-hot encoding untuk kolom kategorik
        # Gunakan transform untuk data baru, bukan fit_transform
        encoded_mode = model_components['encoder_mode'].transform(input_data_processed[['Mode']])
        encoded_category = model_components['encoder_category'].transform(input_data_processed[['Category']])
        encoded_subcategory = model_components['encoder_subcategory'].transform(input_data_processed[['Subcategory']])
        
        # Buat DataFrame dengan encoded columns
        encoded_df = pd.DataFrame(
            np.hstack([encoded_mode, encoded_category, encoded_subcategory]),
            columns=np.concatenate([
                model_components['mode_columns'], 
                model_components['category_columns'], 
                model_components['subcategory_columns']
            ])
        )
        
        # Gabungkan data numerik dengan encoded data
        processed_data = pd.concat([
            input_data_processed.drop(['Mode', 'Category', 'Subcategory'], axis=1),
            encoded_df
        ], axis=1)
        
        return processed_data
    except Exception as e:
        print(f"Error in data preparation: {e}")
        return None

def make_prediction(input_data, model_components, days_to_predict=15):
    try:
        # Extract model components
        model = model_components['model']
        params = model_components['params']
        scaler = model_components['scaler']
        
        # Preprocess input data
        processed_data = prepare_new_data(input_data, model_components)
        
        # Normalisasi dengan menggunakan riwayat data sebelumnya
        # Tambahkan parameter untuk mempertimbangkan variasi
        processed_data['Amount'] = scaler.transform(processed_data[['Amount']])

        # Tambahkan noise atau variasi kecil untuk mencegah prediksi statis
        np.random.seed(None)  # Gunakan seed acak
        noise = np.random.normal(0, 0.1, processed_data['Amount'].shape)
        processed_data['Amount'] += noise

        # Create sequences untuk prediksi
        WINDOW_SIZE = params['window_size']
        X_pred = processed_data.drop(columns=['Amount'])
        X_pred_seq = np.array([X_pred.values[-WINDOW_SIZE:]])
        
        # Predict dengan variasi
        predictions = model.predict(X_pred_seq)
        
        # Inverse transform 
        predictions_orig = scaler.inverse_transform(predictions.reshape(-1, 1))
        
        # Tambahkan sedikit variasi pada prediksi
        predictions_orig += np.random.normal(0, predictions_orig.std() * 0.1, predictions_orig.shape)
        
        # Proses selanjutnya sama seperti sebelumnya...
        last_date = input_data['Date'].iloc[-1]
        future_dates = [last_date + timedelta(days=i+1) for i in range(days_to_predict)]
        
        predictions_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted_Amount': predictions_orig.flatten()
        })
        
        predictions_df['Predicted_Amount'] = predictions_df['Predicted_Amount'].apply(lambda x: max(0, x))
        predictions_df['Predicted_Amount'] = predictions_df['Predicted_Amount'].apply(lambda x: round(x, -3)).astype(int)
        
        return predictions_df
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

@app.route('/predict', methods=['POST'])
def predict_expenses():
    try:
        # Load model components
        model_components = load_forecasting_model()
        if not model_components:
            return jsonify({'error': 'Failed to load model components'}), 500
        
        # Get input data from request
        input_data = request.json
        df_input = pd.DataFrame(input_data)
        
        # Make prediction
        predictions = make_prediction(df_input, model_components)
        
        if predictions is None:
            return jsonify({'error': 'Prediction failed'}), 500
        
        # Convert predictions to JSON serializable format
        return jsonify({
            'predictions': predictions.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Ensure model is loaded
        model_components = load_forecasting_model()
        if model_components:
            return jsonify({'status': 'healthy', 'message': 'Model loaded successfully'}), 200
        else:
            return jsonify({'status': 'unhealthy', 'message': 'Failed to load model'}), 500
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'message': str(e)}), 500

@app.route('/')
def home():
    return "Selamat datang di Aplikasi Prediksi Pengeluaran"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)