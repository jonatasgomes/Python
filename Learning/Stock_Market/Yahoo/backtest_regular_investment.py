import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

ticker = 'AAPL'
start_date = '2022-01-01'
end_date = date.today()
interval = '1ME'
amount = 2000

data = yf.download(ticker, start=start_date, end=end_date)
data.dropna(inplace=True)
resampled_data = data.resample(interval).last().iloc[:-1]

total_invested = 0
total_shares = 0
log = []
for date, row in resampled_data.iterrows():
    price = row['Adj Close']
    total_shares += amount / price
    total_invested += amount
    log.append({
        'Date': date,
        'Price': price,
        'Shares': total_shares,
        'Total Invested': total_invested,
        'Portfolio Value': total_shares * price
    })

df = pd.DataFrame(log)
print('Total Invested:', f'{total_invested:,.2f}')
print('Portfolio Value:', f'{df["Portfolio Value"].iloc[-1]:,.2f}')

plt.figure(figsize=(10, 6))
plt.title(f'{ticker} Portfolio Value')
plt.plot(df['Date'], df['Portfolio Value'], label='Portfolio Value')
plt.plot(df['Date'], df['Total Invested'], color='r', linestyle='dashed', label='Total Invested')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.grid(True)
plt.show()

