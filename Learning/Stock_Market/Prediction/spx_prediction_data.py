import yfinance as yf
import pandas as pd
from datetime import date

# Define the ticker symbols
tickers = {
    "SPX": "^GSPC",       # S&P 500 Index
    "DXY": "DX-Y.NYB",    # US Dollar Index
    "VIX": "^VIX",        # Volatility Index
    "ES1": "ES=F",        # E-mini S&P 500 Futures
    "US10Y": "^TNX"       # 10-Year Treasury Yield
}

# Define the time period for the data
start_date = "2024-01-01"
end_date = date.today().strftime("%Y-%m-%d")

# Fetch data and merge into a single DataFrame
data = pd.DataFrame()
for name, ticker in tickers.items():
    # Download historical data for each ticker
    ticker_data = yf.download(ticker, start=start_date, end=end_date)["Close"]
    data[name] = ticker_data

# Drop rows with missing values (in case of holidays or missing data)
data.dropna(inplace=True)

# Display the first few rows
print(data.head())

# Optionally, save the data to a CSV file for future use
data.to_csv("spx_prediction_data.csv")
