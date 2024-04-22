from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
import datetime as dt
import alpaca_config

client = StockHistoricalDataClient(api_key=alpaca_config.API_KEY, secret_key=alpaca_config.API_SECRET)
request_params = StockBarsRequest(
    symbol_or_symbols='ARM',
    timeframe=TimeFrame.Hour,
    start=dt.datetime(2024, 4, 19),
)
bars = client.get_stock_bars(request_params)
if bars is not None and not bars.df.empty:
    timestamp = [row[1] for row in bars.df.index]
    close = bars.df['close']
    volume = bars.df['volume']
    for now in range(0, len(bars.df.index)):
        print(f'{timestamp[now]:%Y-%m-%d %H:%M} {(close.iloc[now] - close.iloc[now - 5]):.2f} {(close.iloc[now]):.2f}')
else:
    print('No data available')
