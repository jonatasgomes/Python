import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import datetime
import yfinance as yf

start_date = '2024-01-01'
end_date = datetime.datetime.today().strftime('%Y-%m-%d')

# Download historical data for SPX
spx_data = yf.download('^GSPC', start=start_date, end=end_date)
spx_data = spx_data.loc[:, ['Close', 'Open', 'High', 'Low']]
spx_data.loc[:, 'Prev Close'] = spx_data['Close'].shift(1)

# Download historical data for DXY
dxy_data = yf.download('DX-Y.NYB', start=start_date, end=end_date)
dxy_data = dxy_data[['Open']]

# Download historical data for VIX
vix_data = yf.download('^VIX', start=start_date, end=end_date)
vix_data = vix_data[['Open']]

# Download historical data for ES Future
es_future_data = yf.download('ES=F', start=start_date, end=end_date)
es_future_data = es_future_data[['Open']]

# Download historical data for TNX
tnx_data = yf.download('^TNX', start=start_date, end=end_date)
tnx_data = tnx_data[['Open']]

# Merge all dataframes on the date index
merged_data = spx_data.join(dxy_data, rsuffix='_dxy')
merged_data = merged_data.join(vix_data, rsuffix='_vix')
merged_data = merged_data.join(es_future_data, rsuffix='_es')
merged_data = merged_data.join(tnx_data, rsuffix='_tnx')

# Reset index to have 'Date' as a column
merged_data.reset_index(inplace=True)

# Rename columns for clarity
merged_data.rename(columns={
    'Open': 'spx_open',
    'High': 'spx_high',
    'Low': 'spx_low',
    'Close': 'spx_close',
    'Prev Close': 'spx_previous_close',
    'Open_dxy': 'dxy_open',
    'Open_vix': 'vix_open',
    'Open_es': 'es_future_open',
    'Open_tnx': 'tnx_open'
}, inplace=True)

# Select the required columns
final_data = merged_data[['Date', 'spx_previous_close', 'spx_open', 'spx_high', 'spx_low', 'spx_close', 'dxy_open', 'vix_open', 'es_future_open', 'tnx_open']]
final_data = final_data.dropna()

# Get the directory of the running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Save the data to a CSV file in the same directory as the running script
csv_file_path = os.path.join(script_dir, 'demo_01_data.csv')
final_data.to_csv(csv_file_path, index=False)
