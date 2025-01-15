from datetime import datetime, timedelta
import yfinance as yf
import Database.database_connection as db

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
today = datetime.now().strftime('%Y-%m-%d')
ndx_stocks = db.get_ndx_stocks()
ndx_stocks.append({'ticker': '^NDX', 'id': 1, 'weight': 100})

initial_date = input(f"Enter the initial date [{yesterday}]: ") or yesterday
final_date = input(f"Enter the final date [{today}]: ") or today

# get daily data
for stock in ndx_stocks:
  timeframe = '1d'
  data = yf.download(stock['ticker'], start=initial_date, end=final_date, interval=timeframe)
  db.save_stock_prices(stock['id'], data, timeframe)

# get 11:30am data
for stock in ndx_stocks:
  timeframe = '30m'
  data = yf.download(stock['ticker'], start=initial_date, end=final_date, interval=timeframe)
  data = data.between_time('11:30', '11:30')
  db.save_stock_prices(stock['id'], data, timeframe)

print('Data saved successfully')
