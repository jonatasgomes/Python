import yfinance as yf
import os

def price_strategy(option_symbol):
    # Attempt to download the option using yfinance
    try:
        # Retrieve historical option data for six months
        option_data = yf.download(option_symbol, period="6mo", interval="1d")

        # Check if option_data contains sufficient data
        if option_data.empty:
            print(f"Data for option {option_symbol} could not be retrieved.")
            return

        # Initialize position, bought price, and last sold price
        position = 1
        bought_price = 40
        last_sold_price = bought_price
        option_data['Signal'] = ""
        option_data['Profit'] = 0.0

        # Calculate the percentage change in closing price from the previous day
        option_data['Change'] = option_data['Close'].pct_change() * 100

        # Loop through the data and check for buy/sell signals
        for date, row in option_data.iterrows():
            if position == 0:
                # Check for a decrease from the last sold price to buy
                if row['Close'] <= last_sold_price * (1 - decrease_pct / 100):
                    position = 1
                    bought_price = row['Close']
                    option_data.at[date, 'Signal'] = "Buy"
                    print(f"Buy Signal for {option_symbol} on {date.strftime('%Y-%m-%d')} at {bought_price}")
                else:
                    last_sold_price = row['Close']
            elif position == 1:
                # Check for an increase from the bought price to sell
                if row['Close'] >= bought_price * (1 + increase_pct / 100):
                    position = 0
                    profit = row['Close'] - bought_price
                    last_sold_price = row['Close']
                    option_data.at[date, 'Signal'] = "Sell"
                    option_data.at[date, 'Profit'] = profit
                    print(f"Sell Signal for {option_symbol} on {date.strftime('%Y-%m-%d')} at {row['Close']} with profit {profit}")

        # Save only the required columns to a CSV file with 2 decimal places
        path = os.path.join(os.path.dirname(__file__), f"{option_symbol}_price_strategy.csv")
        option_data[['Close', 'Change', 'Signal', 'Profit']].to_csv(path, float_format='%.2f')

    except Exception as e:
        print(f"An error occurred: {e}")

# Trade params
option_symbol = "SPX260116C07000000"
increase_pct = 2
decrease_pct = 1
price_strategy(option_symbol)
