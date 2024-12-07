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
        required_columns = ['Date', 'Mode', 'Category', 'Subcategory', 'Amount', 'Note', 'Currency']
        missing_cols = [col for col in required_columns if col not in input_data.columns]
        if missing_cols:
            raise ValueError(f"Input data is missing the following columns: {missing_cols}")

        # Convert datetime
        input_data['Date'] = pd.to_datetime(input_data['Date'])
        
        # Aggregate data
        input_data['year'] = input_data['Date'].dt.year
        input_data['month'] = input_data['Date'].dt.month
        input_data['day'] = input_data['Date'].dt.day
        input_data['dayofweek'] = input_data['Date'].dt.dayofweek
        
        # Drop unnecessary columns
        input_data = input_data.drop(columns=['Note', 'Currency', 'Date'])
        
        # One-hot encoding for categorical columns
        encoded_mode = model_components['encoder_mode'].transform(input_data[['Mode']])
        encoded_category = model_components['encoder_category'].transform(input_data[['Category']])
        encoded_subcategory = model_components['encoder_subcategory'].transform(input_data[['Subcategory']])
        
        # Concat all encoded results
        encoded_df = pd.DataFrame(
            np.hstack([encoded_mode, encoded_category, encoded_subcategory]),
            columns=np.concatenate([
                model_components['mode_columns'], 
                model_components['category_columns'], 
                model_components['subcategory_columns']
            ])
        )
        
        # Concat encoded results with original df
        processed_data = pd.concat([
            input_data.drop(['Mode', 'Category', 'Subcategory'], axis=1),
            encoded_df
        ], axis=1)
        
        return processed_data
    except Exception as e:
        print(f"Error in data preparation: {e}")
        return None

def make_prediction(input_data, model_components, days_to_predict=15):
    try:
        # Check input data min 15 days
        if len(input_data) < 15:
            raise ValueError(f"Input data must minimum 15 days. Currently only {len(input_data)} days.")

        # Extract model components
        model = model_components['model']
        params = model_components['params']
        scaler = model_components['scaler']
        
        # Preprocess input data
        processed_data = prepare_new_data(input_data, model_components)
        
        # Normalize Amount
        processed_data['Amount'] = scaler.transform(processed_data[['Amount']])

        # Create sequences for prediction
        WINDOW_SIZE = params['window_size']
        X_pred = processed_data.drop(columns=['Amount'])
        X_pred_seq = np.array([X_pred.values[-WINDOW_SIZE:]])
        
        # Predict 
        predictions = model.predict(X_pred_seq)
        
        # Inverse transform 
        predictions_orig = scaler.inverse_transform(predictions.reshape(-1, 1))
        
        # Create future dates
        last_date = input_data['Date'].iloc[-1]
        future_dates = [last_date + timedelta(days=i+1) for i in range(days_to_predict)]
        
        predictions_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted_Amount': predictions_orig.flatten()
        })
        
        # Ensure no negative predictions (negative change to 0)
        predictions_df['Predicted_Amount'] = predictions_df['Predicted_Amount'].apply(lambda x: max(0, x))
        
        # Round to nearest 1000
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)