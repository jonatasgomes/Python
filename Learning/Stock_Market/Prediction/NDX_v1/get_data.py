from datetime import datetime, timedelta
import yfinance as yf
import Database.database_connection as db

initial = (datetime.now() - timedelta(0)).strftime('%Y-%m-%d')
final = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
ndx_stocks = db.get_ndx_stocks()
ndx_stocks.append({'ticker': '^NDX', 'id': 1, 'weight': 100})

initial_date = input(f"Enter the initial date [{initial}]: ") or initial
final_date = input(f"Enter the final date [{final}]: ") or final
data_type = input("Enter the data type: [m]iddle day | [d]aily only | [b]oth: ") or 'm'

# get daily data
if data_type == 'd' or data_type == 'b':
  for stock in ndx_stocks:
    timeframe = '1d'
    data = yf.download(stock['ticker'], start=initial_date, end=final_date, interval=timeframe)
    db.save_stock_prices(stock['id'], data, timeframe)

# get 11:30am data
if data_type == 'm' or data_type == 'b':
  for stock in ndx_stocks:
    timeframe = '30m'
    data = yf.download(stock['ticker'], start=initial_date, end=final_date, interval=timeframe)
    data = data.at_time('11:30')
    db.save_stock_prices(stock['id'], data, timeframe)

print('Data saved successfully')
