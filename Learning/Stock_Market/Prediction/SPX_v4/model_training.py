import pandas as pd
import xgboost as xgb
from datetime import datetime
import os

# Function to train the model
def train_model(data_path):
    # Load the training data
    print("Loading training data...")
    data = pd.read_csv(data_path)

    # Separate features and target variables
    X = data.drop(columns=['SPX_Daily_Low', 'SPX_Daily_High', 'Date'])
    y_low = data['SPX_Daily_Low']
    y_high = data['SPX_Daily_High']

    # Train XGBoost models for SPX_Daily_Low and SPX_Daily_High
    print("Training model for SPX_Daily_Low...")
    model_low = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
    model_low.fit(X, y_low)

    print("Training model for SPX_Daily_High...")
    model_high = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
    model_high.fit(X, y_high)

    return model_low, model_high

# Function to make predictions
def predict_spx(model_low, model_high, input_path):
    # Load the input data for prediction
    print("Loading prediction data...")
    input_data = pd.read_csv(input_path)

    # Ensure input data is aligned with training columns
    prediction_features = input_data.drop(columns=['Date'])

    # Predict SPX_Daily_Low and SPX_Daily_High
    print("Predicting SPX_Daily_Low...")
    predicted_low = model_low.predict(prediction_features)

    print("Predicting SPX_Daily_High...")
    predicted_high = model_high.predict(prediction_features)

    # Output predictions
    predictions = pd.DataFrame({
        'Date': input_data['Date'],
        'SPX_Daily_Low': predicted_low,
        'SPX_Daily_High': predicted_high
    })

    print("Predictions:")
    print(predictions)

# Main execution
if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    training_csv_path = os.path.join(script_dir, "spx_training_data.csv")
    prediction_csv_path = os.path.join(script_dir, "spx_prediction_data.csv")

    # Train the model
    model_low, model_high = train_model(training_csv_path)

    # Predict using the model
    predict_spx(model_low, model_high, prediction_csv_path)
