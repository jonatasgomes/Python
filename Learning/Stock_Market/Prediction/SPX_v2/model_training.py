import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import os

# Step 1: Load the saved data
file_path = os.path.join(os.path.dirname(__file__), "spx_top_100_data.csv")
data = pd.read_csv(file_path, parse_dates=['Date'])

# Filter SPX data only
spx_data = data[data['Ticker'] == '^GSPC']

# Step 2: Feature Engineering
# Sort data by date
spx_data = spx_data.sort_values(by='Date')

# Create lagging features
for lag in range(1, 6):  # Lag features for the past 5 days
    spx_data[f'Close_Lag_{lag}'] = spx_data['Close'].shift(lag)

# Drop rows with NaN values from lagging
spx_data = spx_data.dropna()

# Define features and targets
features = [col for col in spx_data.columns if 'Lag' in col]
X = spx_data[features]
y_high = spx_data['High']
y_low = spx_data['Low']

# Split data into training and testing sets
X_train, X_test, y_high_train, y_high_test, y_low_train, y_low_test = train_test_split(
    X, y_high, y_low, test_size=0.2, random_state=42
)

# Step 3: Train XGBoost Model
print("Training XGBoost Model...")
xgb_high = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
xgb_low = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

# Train models
xgb_high.fit(X_train, y_high_train)
xgb_low.fit(X_train, y_low_train)

# Step 4: Evaluate XGBoost Model
print("Evaluating XGBoost Model...")
y_high_pred_xgb = xgb_high.predict(X_test)
y_low_pred_xgb = xgb_low.predict(X_test)

print("XGBoost High RMSE:", np.sqrt(mean_squared_error(y_high_test, y_high_pred_xgb)))
print("XGBoost Low RMSE:", np.sqrt(mean_squared_error(y_low_test, y_low_pred_xgb)))

# Step 5: Predict SPX next day's high and low
print("Predicting SPX next day's values...")
latest_data = X.iloc[-1].values.reshape(1, -1)  # XGBoost requires 2D input

next_high_xgb = xgb_high.predict(latest_data)[0]
next_low_xgb = xgb_low.predict(latest_data)[0]

predicted_date = spx_data['Date'].max() + pd.Timedelta(days=1)
print(f"Predicted Date: {predicted_date.strftime('%Y-%m-%d')}")
print(f"XGBoost - Predicted High: {next_high_xgb}, Predicted Low: {next_low_xgb}")
