import yfinance as yf
import datetime as dt
import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

g_symbol = 'ARM'
g_rsi_period = 14
g_data_start = '2024-07-01'
g_data_path = f'./datasets/{g_symbol}.csv'
g_data = None
g_file_updated = False
g_show_fig = False
g_log = []

def save_data():
    global g_data
    os.makedirs(os.path.dirname(g_data_path), exist_ok=True)
    g_data.to_csv(g_data_path, sep=',', decimal='.', index=True)

def download_data():
    global g_data
    g_data = yf.download(g_symbol, start=g_data_start, end=dt.datetime.now(), interval='5m')
    calc_rsi()
    save_data()
    g_log.append(f'{dt.datetime.now()} Downloaded {g_symbol} data from Yahoo Finance')

def calc_rsi():
    global g_data
    g_data['CloseDelta'] = g_data.Close / g_data.Close.shift(1) - 1
    g_data['CloseDeltaUp'] = g_data.CloseDelta.apply(lambda x: x if x > 0 else 0)
    g_data['CloseDeltaDown'] = g_data.CloseDelta.apply(lambda x: x if x < 0 else 0)
    g_data['CloseDeltaUpMean'] = g_data.CloseDeltaUp.rolling(g_rsi_period).mean()
    g_data['CloseDeltaDownMean'] = g_data.CloseDeltaDown.rolling(g_rsi_period).mean()
    g_data['RSI'] = 100 - (100 / (1 + g_data.CloseDeltaUpMean / abs(g_data.CloseDeltaDownMean)))
    g_data.drop(['CloseDelta', 'CloseDeltaUp', 'CloseDeltaDown', 'CloseDeltaUpMean', 'CloseDeltaDownMean'], axis=1, inplace=True)

def backtest():
    global g_data
    l_exit = 70
    l_entry = 30
    l_bet_size = 100
    l_trades = 0
    l_balance = 0
    l_last_price = 0
    l_list_trades = []

    for l_time, l_row in g_data.iterrows():
        if l_row.RSI <= l_entry and l_trades == 0:
            l_trades = 1
            l_balance += -1 * l_bet_size * l_row.Close
            l_last_price = l_row.Close
            l_list_trades += [{'time': l_time, 'kind': 'buy', 'quantity': l_bet_size, 'price': l_row.Close, 'balance': ''}]
        elif l_row.RSI > l_exit and l_trades == 1 and l_row.Close > l_last_price:
            l_trades = 0
            l_balance += l_bet_size * l_row.Close
            l_list_trades += [{'time': l_time, 'kind': 'sell', 'quantity': l_bet_size, 'price': l_row.Close, 'balance': l_balance}]

    return l_list_trades

# check if file exists and is updated
if os.path.exists(g_data_path):
    l_file_date = dt.datetime.fromtimestamp(os.path.getmtime(g_data_path))
    if l_file_date.date() == dt.datetime.now().date():
        g_file_updated = True
    else:
        os.remove(g_data_path)

# load data
if g_file_updated:
    # from file
    file_date = dt.datetime.fromtimestamp(os.path.getmtime(g_data_path))
    g_data = pd.read_csv(g_data_path, sep=',', decimal='.', index_col=0, parse_dates=True)
    g_log.append(f'{dt.datetime.now()} Loaded {g_symbol} data from {g_data_path} created at {file_date}')
else:
    # from download
    download_data()

if g_show_fig:
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.02, shared_xaxes=True)
    fig.add_trace(go.Candlestick(x=g_data.index, open=g_data.Open, high=g_data.High, low=g_data.Low, close=g_data.Close, name='OHLC'), row=1, col=1)
    fig.add_trace(go.Scatter(x=g_data.index, y=g_data.RSI, name='RSI'), row=2, col=1)
    fig.update_layout(title=f'{g_symbol} - RSI', showlegend=False, xaxis_rangeslider_visible=False)
    fig.update_xaxes(rangebreaks=[dict(bounds=[16, 9.5], pattern="hour"), dict(bounds=["sat", "mon"])])
    fig.show()

print(g_log)
g_trades = backtest()
print(pd.DataFrame(g_trades))
