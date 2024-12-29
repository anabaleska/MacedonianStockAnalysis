import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.api.models import Sequential
from keras.api.layers import LSTM, Dense
from flask import Flask, request, jsonify
import psycopg2  # PostgreSQL library
import joblib

app = Flask(__name__)

# Database connection settings
DB_SETTINGS = {
    'dbname': 'msa_data',
    'user': 'postgres',
    'password': 'anaiman',
    'host': 'localhost',
    'port': '5432'
}

# LSTM model creation function (used only for training, not in the prediction route)
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(64, return_sequences=True, activation="relu"))
    model.add(LSTM(64, return_sequences=False, activation="relu"))
    model.add(Dense(16, activation="linear"))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=["mean_squared_error"])
    return model


# Ensure that the model is loaded when making predictions
def load_model():
    try:
        model = joblib.load('lstm_model.pkl')  # Adjust path if needed
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None


# Fetch historical price data from the database
def fetch_historical_data(ticker):
    try:
        # Connect to the database
        connection = psycopg2.connect(**DB_SETTINGS)
        cursor = connection.cursor()

        # Query to fetch historical price data
        query = """
        SELECT last_transaction, date
        FROM ticker_data
        WHERE ticker = %s
        ORDER BY date DESC
        LIMIT 1000;
        """
        cursor.execute(query, (ticker,))
        rows = cursor.fetchall()

        # Convert the data to a pandas DataFrame
        historical_prices = pd.DataFrame(rows, columns=['last_transaction', 'date'])
        historical_prices['date'] = pd.to_datetime(historical_prices['date'])

        cursor.close()
        connection.close()

        return historical_prices

    except Exception as e:
        print(f"Error fetching historical data: {str(e)}")
        return None


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        ticker = data.get('ticker')  # Get ticker symbol

        # Fetch historical data from database
        historical_prices = fetch_historical_data(ticker)
        if historical_prices is None or historical_prices.empty:
            return jsonify({'error': 'Historical price data is missing or empty'}), 400

        # Ensure there are at least 60 data points
        if len(historical_prices) < 60:
            return jsonify({'error': 'Insufficient historical data (minimum 60 points required)'}), 400

        # Prepare the data
        prices = historical_prices['close'].values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(prices)

        # Create test data with sliding window
        X_test = []
        test_data = scaled_data[-60:]  # Use only the last 60 points for prediction
        X_test.append(test_data)
        X_test = np.array(X_test)
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        # Load the model
        model = load_model()
        if model is None:
            return jsonify({'error': 'Model loading failed'}), 500

        # Predict
        prediction = model.predict(X_test)
        prediction = scaler.inverse_transform(prediction)

        return jsonify({
            'predicted_price': prediction.flatten().tolist()[0],
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
