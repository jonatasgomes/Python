import pandas_datareader.data as web
from datetime import datetime
import env

api_key = env.api_key
ticker = 'AAPL'
data_source = 'av-daily'
start_date = datetime(2024, 4, 18)
end_date = datetime.now()

try:
    stock_data = web.DataReader(ticker, data_source, start=start_date, end=end_date, api_key=api_key)
    print(stock_data.head())
except Exception as e:
    print(f'An error occurred: {e}')
