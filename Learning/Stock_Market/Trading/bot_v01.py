import yfinance as yf
import pandas as pd

BUY = 'BUY'
SELL = 'SELL'
HOLD = 'HOLD'

def signal_generator(df):
  open = df.Open.iloc[-1]
  close = df.Close.iloc[-1]
  previous_open = df.Open.iloc[-2]
  previous_close = df.Close.iloc[-2]
  if open > close and previous_open < previous_close and close < previous_open and open >= previous_close:
    return BUY
  elif open < close and previous_open > previous_close and close > previous_open and open <= previous_close:
    return SELL
  else:
    return HOLD

data = yf.download('EURUSD=X', start='2025-01-21', end='2025-01-22', interval='15m')
signal = []
signal.append(BUY)
for i in range(1, len(data)):
  df = data[i - 1:i + 1]
  signal.append(signal_generator(df))
data['signal'] = signal

print(data.signal.value_counts())
