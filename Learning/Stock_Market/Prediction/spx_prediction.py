import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load your historical data
data = pd.read_csv("spx_prediction_data.csv")  # Replace with your file path

# Drop the Date column if present
if 'Date' in data.columns:
    data.drop(columns=['Date'], inplace=True)

# Create lagged features for short-term prediction
def create_lagged_features(df, lag_days=5):
    for col in ["SPX", "DXY", "VIX", "ES1", "US10Y"]:
        for lag in range(1, lag_days + 1):
            df[f"{col}_lag{lag}"] = df[col].shift(lag)
    df.dropna(inplace=True)  # Drop rows with NaN values after shifting
    return df

data = create_lagged_features(data)

# Define features (X) and target (y)
X = data.drop(columns=["SPX"])  # Drop SPX for independent variables
y = data["SPX"]  # Target variable is SPX

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Set up the XGBoost model
model = xgb.XGBRegressor(
    objective="reg:squarederror",
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate model performance
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"Root Mean Squared Error: {rmse}")

plt.plot(y_test.values, label="Actual SPX")
plt.plot(y_pred, label="Predicted SPX")
plt.xlabel("Time")
plt.ylabel("SPX Value")
plt.legend()
plt.show()