import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt

stock = 'AAPL'
aapl = yf.Ticker(stock)
# print(aapl.fast_info.keys())
# [print(f'aapl.fast_info[{k}] = {aapl.fast_info[k]}') for k in aapl.fast_info.keys()]
# print(aapl.get_financials())

plt.style.use('ggplot')
financials = aapl.get_financials()

# plt.plot(financials.loc['EBITDA'].index, financials.loc['EBITDA'].values, marker='o')
# plt.xticks(rotation=45)
# plt.title(f'{stock} EBITDA')
# plt.show()

revenue = financials.loc['CostOfRevenue':'TotalRevenue']
revenue = revenue / 1000000000
revenue = revenue.T
print(revenue)

plt.figure(figsize=(20, 10))
x_values = [i.year for i in revenue.index]
data = revenue
x = np.arange(len(x_values))
width = 0.25
multiplier = 0
fig, ax = plt.subplots(layout='constrained')
for attribute, measurement in data.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

ax.set_ylabel('USD Billions')
ax.set_title(f'{stock} Revenue Analisys')
ax.set_xticks(x + width, x_values)
ax.legend(revenue.columns, loc=9, ncols=3)
ax.set_ylim(0, 500)
plt.show()
