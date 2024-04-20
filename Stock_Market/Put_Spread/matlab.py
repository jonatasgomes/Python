import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download("NVDA", start="2024-01-01", end="2024-04-05")
data['Close'].plot()
plt.title("Stock Prices")
plt.show()