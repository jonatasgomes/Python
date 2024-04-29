from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
import datetime as dt
import numpy as np
import env

# https://www.youtube.com/watch?v=txIbRqQVKKI
client = StockHistoricalDataClient(api_key=env.API_KEY, secret_key=env.API_SECRET)
request_params = StockBarsRequest(
    symbol_or_symbols='META',
    timeframe=TimeFrame.Day,
    start=dt.datetime(2024, 1, 1),
)
bars = client.get_stock_bars(request_params)
ts = [row[1] for row in bars.df.index]
open = bars.df['open']
low = bars.df['low']
close = bars.df['close']
high = bars.df['high']
wins = 0
position = []
profits = []
max_cash = 500.00
for now in range(0, len(bars.df.index)):
    if len(position) > 0:
        buy_avg = np.mean(position)
    else:
        buy_avg = 0
    change = round(1 - (open.iloc[now] / low.iloc[now]), 5)
    if buy_avg > 0:
        pl = round(1 - (buy_avg / close.iloc[now]), 5)
    else:
        pl = 0
    if len(position) == 0 and change < -0.01:
        position.append(close.iloc[now])
    elif len(position) > 0.0 and pl < -0.0025:
        if sum(position) + close.iloc[now] < max_cash:
            position.append(close.iloc[now])
    elif pl >= 0.01:
        profits.append(close.iloc[now] - buy_avg)
        wins += 1
        position.clear()
    print(ts[now].date(), len(position), change, pl, wins)

print(f'Profits: {sum(profits):.2f}')