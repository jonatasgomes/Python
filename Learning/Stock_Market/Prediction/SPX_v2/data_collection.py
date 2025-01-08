import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

# Step 1: Define the SPX ticker and the top 100 stock tickers
SPX_TICKER = '^GSPC'  # S&P 500 Index
top_100_stocks = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK-B', 'UNH', 'JNJ',
    'V', 'PG', 'XOM', 'JPM', 'MA', 'HD', 'CVX', 'LLY', 'ABBV', 'MRK', 'PEP', 'KO',
    'BAC', 'COST', 'AVGO', 'TMO', 'DIS', 'ADBE', 'WMT', 'PFE', 'CSCO', 'NFLX', 'ABT',
    'DHR', 'ACN', 'NKE', 'MCD', 'VZ', 'INTC', 'TXN', 'CMCSA', 'CRM', 'QCOM', 'UPS',
    'AMGN', 'LIN', 'NEE', 'ORCL', 'MS', 'PM', 'HON', 'BMY', 'WFC', 'SCHW', 'IBM',
    'RTX', 'MDT', 'CVS', 'C', 'LOW', 'UNP', 'INTU', 'T', 'CAT', 'ELV', 'LMT', 'BLK',
    'SPGI', 'PLD', 'AXP', 'DE', 'ISRG', 'ZTS', 'AMD', 'ADP', 'BKNG', 'GS', 'GE', 'NOW',
    'USB', 'MMM', 'SYK', 'TGT', 'MO', 'ADI', 'MMC', 'AMT', 'CB', 'DUK', 'SO', 'EW',
    'CI', 'CL', 'APD', 'REGN', 'MDLZ', 'PGR', 'TRV'
]

# Step 2: Define the data collection period
end_date = datetime.today()
start_date = end_date - timedelta(days=720)

# Step 3: Create a function to fetch data for a single ticker
def fetch_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end, interval='1d', progress=False)
        data['Ticker'] = ticker
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Step 4: Fetch data for SPX and all 100 stocks
all_data = []

# Fetch SPX data
print("Fetching SPX data...")
spx_data = fetch_data(SPX_TICKER, start_date, end_date)
if spx_data is not None:
    all_data.append(spx_data)

# Fetch top 100 stock data
print("Fetching top 100 stock data...")
for ticker in top_100_stocks:
    print(f"Fetching data for {ticker}...")
    stock_data = fetch_data(ticker, start_date, end_date)
    if stock_data is not None:
        all_data.append(stock_data)

# Step 5: Combine all data into a single DataFrame
# Filter out empty DataFrames from the list
all_data = [df for df in all_data if not df.empty]

if all_data:
    combined_data = pd.concat(all_data)
    # Step 6: Save the data to a CSV file
    # Save the file in the same folder as the script
    output_file = os.path.join(os.path.dirname(__file__), "spx_top_100_data.csv")
    combined_data.to_csv(output_file, index_label="Date")
    print(f"Data saved to {output_file}")
else:
    print("No valid data fetched. Skipping CSV generation.")
