import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

# Function to fetch historical data for a stock
def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval="30m")
    stock_data.index = stock_data.index.tz_localize(None)  # Ensure tz-naive timestamps
    return stock_data

# Function to process data for a specific stock
def process_stock_data(ticker, start_date, end_date):
    data = fetch_stock_data(ticker, start_date, end_date)

    # Extract open price and 11:30 price
    data['Time'] = data.index.strftime('%H:%M')
    open_prices = data.groupby(data.index.date)['Open'].first()
    price_at_1130 = data[data['Time'] == '11:30']['Close']

    # Combine data into a single row per date
    processed_data = pd.DataFrame({
        f'{ticker}_Open_Price': open_prices
    })
    price_at_1130 = price_at_1130.reset_index()
    price_at_1130['Date'] = price_at_1130['Datetime'].dt.date
    price_at_1130.set_index(pd.to_datetime(price_at_1130['Date']), inplace=True)
    processed_data[f'{ticker}_1130_Price'] = price_at_1130['Close']

    processed_data = processed_data.reset_index()
    processed_data.rename(columns={'index': 'Date'}, inplace=True)
    processed_data['Date'] = pd.to_datetime(processed_data['Date'])
    processed_data.set_index('Date', inplace=True)
    processed_data.dropna(inplace=True)

    return processed_data

# Function to fetch and process SPX data
def fetch_spx_data(start_date, end_date):
    spx_data = yf.download('^GSPC', start=start_date, end=end_date, interval="30m")
    spx_data.index = spx_data.index.tz_localize(None)  # Ensure tz-naive timestamps
    spx_data['Time'] = spx_data.index.strftime('%H:%M')
    spx_data['Date'] = spx_data.index.date  # Add a Date column for grouping

    open_prices = spx_data.groupby('Date')['Open'].first()
    price_at_1130 = spx_data[spx_data['Time'] == '11:30'].set_index('Date')['Close']
    low_prices = spx_data.groupby('Date')['Low'].min()
    high_prices = spx_data.groupby('Date')['High'].max()

    # Combine SPX data into a single DataFrame
    spx_processed = pd.DataFrame({
        'SPX_Open_Price': open_prices,
        'SPX_1130_Price': price_at_1130,
        'SPX_Daily_Low': low_prices,
        'SPX_Daily_High': high_prices
    })

    spx_processed.index = pd.to_datetime(spx_processed.index)  # Ensure index is datetime

    return spx_processed

# Define date range
start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
end_date = (datetime.now() - timedelta(days=-1)).strftime('%Y-%m-%d')

# List of stocks to process
stocks = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'META', 'GOOGL', 'BRK-B', 'GOOG', 'LLY', 'AVGO', 'JPM', 'TSLA', 'UNH', 'XOM', 'V', 'PG', 'COST', 'JNJ', 'ES=F']

# Initialize final DataFrame
final_data = None

# Process each stock
for stock in stocks:
    print(f"Fetching {stock} data...")
    stock_data = process_stock_data(stock, start_date, end_date)
    if final_data is None:
        final_data = stock_data
    else:
        final_data = pd.concat([final_data, stock_data], axis=1)

# Fetch SPX data
print("Fetching SPX data...")
spx_data = fetch_spx_data(start_date, end_date)

# Combine all data
print("Combining data...")
final_data = pd.concat([final_data, spx_data], axis=1)
final_data.index.name = 'Date'

# Save to CSV
output_file = os.path.join(os.path.dirname(__file__), 'buffer_data.csv')
print(f"Saving data to {output_file}...")
final_data.to_csv(output_file)
print("Done!")
