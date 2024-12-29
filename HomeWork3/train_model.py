import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.api.models import Sequential
from keras.api.layers import LSTM, Dense
import joblib
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:anaiman@localhost:5432/msa_data"
engine = create_engine(DATABASE_URL)

# Fetch the stock price data from your database
query = "SELECT last_transaction FROM ticker_data ORDER BY date DESC"
df = pd.read_sql(query, engine)

# Assuming your dataframe `df` contains a column 'close' with stock closing prices
prices = df['last_transaction'].values.reshape(-1, 1)

# Scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(prices)

# Prepare the data for LSTM
X_train = []
y_train = []
for i in range(60, len(scaled_data)):
    X_train.append(scaled_data[i-60:i, 0])  # Last 60 days data
    y_train.append(scaled_data[i, 0])  # Predicted price

X_train = np.array(X_train)
y_train = np.array(y_train)

# Reshape for LSTM
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

# LSTM Model Creation
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(64, return_sequences=True, activation="relu"))
model.add(LSTM(64, return_sequences=False, activation="relu"))
model.add(Dense(16, activation="linear"))
model.add(Dense(1))

# Compile and train the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=["mean_squared_error"])
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Save the model
joblib.dump(model, 'lstm_model.pkl')
