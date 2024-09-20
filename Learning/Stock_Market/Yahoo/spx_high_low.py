import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np


# Fetch SPX historical data
def fetch_spx_data():
    global spx_data
    spx = yf.Ticker('^GSPC')
    spx_data = spx.history(period='30d', interval='1h')  # 30 days of hourly data
    return spx_data

# Calculate moving averages
def calculate_sma(data, period):
    return data['Close'].rolling(window=period).mean()

spx_data = fetch_spx_data()
spx_data['SMA_5'] = calculate_sma(spx_data, 5)
spx_data['SMA_20'] = calculate_sma(spx_data, 20)

# Signal for potential high and low
spx_data['Signal'] = spx_data['SMA_5'] > spx_data['SMA_20']

print(spx_data[['Close', 'SMA_5', 'SMA_20', 'Signal']].tail())

# Calculate Bollinger Bands
def calculate_bollinger_bands(data, window, num_std_dev):
    sma = data['Close'].rolling(window=window).mean()
    std_dev = data['Close'].rolling(window=window).std()
    upper_band = sma + (std_dev * num_std_dev)
    lower_band = sma - (std_dev * num_std_dev)
    return upper_band, lower_band

spx_data['Upper_Band'], spx_data['Lower_Band'] = calculate_bollinger_bands(spx_data, 20, 2)

print(spx_data[['Close', 'Upper_Band', 'Lower_Band']].tail())

# Calculate the ATR
def calculate_atr(data, window):
    data['high-low'] = data['High'] - data['Low']
    data['high-close'] = abs(data['High'] - data['Close'].shift())
    data['low-close'] = abs(data['Low'] - data['Close'].shift())
    true_range = data[['high-low', 'high-close', 'low-close']].max(axis=1)
    atr = true_range.rolling(window=window).mean()
    return atr

spx_data['ATR'] = calculate_atr(spx_data, 14)
spx_data['Estimated_High'] = spx_data['Close'] + spx_data['ATR']
spx_data['Estimated_Low'] = spx_data['Close'] - spx_data['ATR']

print(spx_data[['Close', 'Estimated_High', 'Estimated_Low']].tail())

# Prepare features for machine learning
def prepare_features(data):
    data['SMA_5'] = calculate_sma(data, 5)
    data['SMA_20'] = calculate_sma(data, 20)
    data['Upper_Band'], data['Lower_Band'] = calculate_bollinger_bands(data, 20, 2)
    data['ATR'] = calculate_atr(data, 14)
    return data[['SMA_5', 'SMA_20', 'Upper_Band', 'Lower_Band', 'ATR']]  # .dropna()

features = prepare_features(spx_data)
target_high = spx_data['High']  # .dropna()
target_low = spx_data['Low']  #.dropna()

# Train/test split
# print(features.shape)
# print(target_low.shape)
# target_high = target_high[:189]
# target_low = target_low[:189]
X_train, X_test, y_train_high, y_test_high = train_test_split(features, target_high, test_size=0.2)
X_train, X_test, y_train_low, y_test_low = train_test_split(features, target_low, test_size=0.2)

# Train the models
model_high = RandomForestRegressor().fit(X_train, y_train_high)
model_low = RandomForestRegressor().fit(X_train, y_train_low)

# Predict the high and low for today
predicted_high = model_high.predict(X_test)
predicted_low = model_low.predict(X_test)

print(f"Predicted High: {predicted_high[-1]}")
print(f"Predicted Low: {predicted_low[-1]}")
