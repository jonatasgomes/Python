import yfinance as yf
import os

def price_strategy(option_symbol):
    # Attempt to download the option using yfinance
    try:
        # Retrieve historical option data
        option_data = yf.download(option_symbol, period=f"{max_months}mo", interval="1d")

        # Check if option_data contains sufficient data
        if option_data.empty:
            print(f"Data for option {option_symbol} could not be retrieved.")
            return

        # Initialize position, bought price, and last sold price
        position = 0
        bought_price = 0
        total_cost = 0
        option_data['Signal'] = ""
        option_data['Signal Price'] = 0.0
        option_data['Profit'] = 0.0
        option_data['Positions'] = position
        option_data['Avg Price'] = 0.0
        option_data['Total Cost'] = 0.0

        # Calculate the percentage change in closing price from the previous day
        option_data['Change'] = option_data['Open'].pct_change() * 100

        # Loop through the data and check for buy/sell signals
        for date, row in option_data.iterrows():
            if position == 0 or (option_data.at[date, 'Change'] < -decrease_pct and position < max_positions):
                position += 1
                bought_price = row['Open']
                total_cost += bought_price
                option_data.at[date, 'Signal'] = "Buy"
                option_data.at[date, 'Signal Price'] = -bought_price
                print(f"Buy Signal for {option_symbol} on {date.strftime('%Y-%m-%d')} at ${bought_price:.2f}")
            elif position > 0 and row['Close'] > (total_cost / position) * (1 + increase_pct / 100):
                profit = row['Close'] - (total_cost / position)
                position -= 1
                total_cost -= row['Close'] - profit
                option_data.at[date, 'Signal'] = "Sell"
                option_data.at[date, 'Signal Price'] = row['Close']
                option_data.at[date, 'Profit'] = profit
                print(f"Sell Signal for {option_symbol} on {date.strftime('%Y-%m-%d')} at ${row['Close']:.2f} with profit of ${profit:.2f}")
            option_data.at[date, 'Positions'] = position
            option_data.at[date, 'Total Cost'] = total_cost
            option_data.at[date, 'Avg Price'] = total_cost / (position if position > 0 else 1)
        option_data.loc['Total', ['Profit', 'Signal Price']] = [option_data['Profit'].sum() * 100, option_data['Signal Price'].sum() * 100]

        # Save only the required columns to a CSV file with 2 decimal places
        path = os.path.join(os.path.dirname(__file__), f"{option_symbol}_price_strategy.csv")
        option_data[['Open', 'Close', 'Change', 'Signal', 'Signal Price', 'Total Cost', 'Positions', 'Avg Price', 'Profit']].to_csv(path, float_format='%.2f')

    except Exception as e:
        print(f"An error occurred: {e}")

# Trade params
option_symbol = "SPX250321C06200000"
max_positions = 5
increase_pct = 4
decrease_pct = 2
max_months = 3 # 1, 3, 6
price_strategy(option_symbol)
