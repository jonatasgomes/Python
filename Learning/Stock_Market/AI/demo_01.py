import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import os

# Load data
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'demo_01_data.csv')
data = pd.read_csv(file_path)

# Feature selection
features = data[['spx_previous_close', 'spx_open', 'spx_close', 'dxy_open', 'vix_open', 'es_future_open', 'tnx_open']]
target = data[['spx_low', 'spx_high']]

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=0)

# Standardize features
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Initialize and train the best model (LinearRegression)
best_model = MultiOutputRegressor(LinearRegression())
best_model.fit(x_train, y_train)

# Evaluate the model
predictions = best_model.predict(x_test)
mse = mean_squared_error(y_test, predictions, multioutput='raw_values')
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions, multioutput='raw_values')
print(f"LinearRegression - RMSE: {rmse}, R2: {r2}")

# Function to make new predictions
def predict_new_data(spx_previous_close, spx_open, spx_close, dxy_open, vix_open, es_future_open, tnx_open):
    feature_names = ['spx_previous_close', 'spx_open', 'spx_close', 'dxy_open', 'vix_open', 'es_future_open', 'tnx_open']
    new_data = pd.DataFrame([[spx_previous_close, spx_open, spx_close, dxy_open, vix_open, es_future_open, tnx_open]], columns=feature_names)
    new_data_scaled = scaler.transform(new_data)
    prediction = best_model.predict(new_data_scaled)
    return prediction

# Example usage
spx_previous_close = 5872.17
spx_open = 5912.71
spx_close = spx_open - 30
dxy_open = 108.103
vix_open = 21.61
es_future_open = 5949.50
tnx_open = 4.512

# spx_previous_close, spx_open, spx_close, dxy_open, vix_open, es_future_open, tnx_open
predicted_high_low = predict_new_data(spx_previous_close, spx_open, spx_close, dxy_open, vix_open, es_future_open, tnx_open)
print(f"Predicted Low and High: {predicted_high_low}")
