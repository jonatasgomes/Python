import yfinance as yf
from datetime import datetime, timedelta
from tabulate import tabulate
import matplotlib.pyplot as plt
import squarify

# Define the companies and their weights in the S&P 500
companies = {
    'AAPL': 6.97,  # Apple
    'MSFT': 6.74,  # Microsoft
    'NVDA': 6.33,  # NVIDIA
    'AMZN': 3.39,  # Amazon
    'META': 2.52,  # Meta Platforms
    'GOOGL': 2.05,  # Alphabet Class A
    'BRK-B': 1.73,  # Berkshire Hathaway
    'GOOG': 1.73,  # Alphabet Class C
    'LLY': 1.62,  # Eli Lilly
    'AVGO': 1.50,  # Broadcom
    'JPM': 1.32,  # JPMorgan Chase
    'TSLA': 1.22,  # Tesla
    'UNH': 1.16,  # UnitedHealth Group
    'XOM': 1.15,  # ExxonMobil
    'V': 0.90,  # Visa
    'PG': 0.87,  # Procter & Gamble
    'COST': 0.83,  # Costco
    'JNJ': 0.83  # Johnson & Johnson
}

# Define the time range for the last 24 hours
end = datetime.now()
start = end - timedelta(minutes=20)


# Function to calculate percentage change (trend)
def calculate_trend(_data):
    if _data.empty or len(_data) < 2:
        return 0
    open_price = _data['Open'].iloc[0]
    close_price = _data['Close'].iloc[-1]
    return ((close_price - open_price) / open_price) * 100


# Collect data and calculate individual trends
trends = []
for company, weight in companies.items():
    # Collect 24-hour data including after-market
    data = yf.download(company, start=start, end=end, interval='5m', prepost=True)

    # Calculate individual trend
    trend = calculate_trend(data)
    trends.append((trend, weight))

# Calculate overall trend (index)
overall_trend = sum(t * w for t, w in trends) / sum(companies.values())

# Collect trends into a single row
row = [f"{overall_trend:.2f}"] + [f"{trend:.2f}" for trend, _ in trends]
headers = ["SPX"] + list(companies.keys())

# Display as a single row
print(tabulate([row], headers=headers, tablefmt="simple"))

# Tree map chart
trends = [(float(trend), weight) for trend, weight in trends]
colors = ['green' if trend[0] > 0 else 'red' if trend[0] < -0.1 else 'gray' for trend in trends]
sizes = list(companies.values())
labels = [f"{name}\n{trend[0]:.2f}%" for name, trend in zip(companies.keys(), trends)]
plt.figure(figsize=(12, 8))
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.7, pad=True)
plt.title("Company Performance: Size by Weight, Color by Trend")
plt.axis('off')  # Remove the axis
plt.show()
