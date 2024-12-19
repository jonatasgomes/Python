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

# Load data - Date,spx_previous_close,spx_open,spx_high,spx_low,spx_close,dxy_open,vix_open,es_future_open,tnx_open
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'demo_01_data.csv')
data = pd.read_csv(file_path).dropna()

# Feature selection
features = data[['spx_previous_close', 'spx_open', 'spx_close', 'dxy_open', 'vix_open', 'es_future_open', 'tnx_open']]
target = data[['spx_low', 'spx_high']]

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=0)

# Standardize features
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Initialize models
models = {
    'SVR': MultiOutputRegressor(SVR(kernel='rbf')),
    'RandomForest': MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=0)),
    'LinearRegression': MultiOutputRegressor(LinearRegression())
}

# Evaluate models
results = {}
for name, model in models.items():
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions, multioutput='raw_values')
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions, multioutput='raw_values')
    results[name] = {'RMSE': rmse, 'R2': r2}

# Print results
for name, metrics in results.items():
    print(f"{name} - RMSE: {metrics['RMSE']}, R2: {metrics['R2']}")

# Choose the best model based on RMSE and R2
best_model_name = min(results, key=lambda x: results[x]['RMSE'].mean())
best_model = models[best_model_name]
print(f"Best model: {best_model_name}")
