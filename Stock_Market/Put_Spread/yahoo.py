import yfinance as yf

def get_amd_options(expiration_date, strikes_range=50):
    # Fetch AMD stock data
    amd_stock = yf.Ticker("AMD")

    # Get the current stock price
    current_price = amd_stock.history(period="1d")['Close'].iloc[0]
    print(f"Current price: {current_price:.2f}")

    # Get options data for AMD
    options_dates = amd_stock.options

    # Check if the desired expiration date is available
    if expiration_date not in options_dates:
        print(f"No options found for {expiration_date}")
        return None

    # Fetch the option chain for the desired expiration date
    opts = amd_stock.option_chain(date=expiration_date)

    # Get put options
    puts = opts.puts

    # Filter puts based on the current price and strike range
    lower_bound = current_price - strikes_range
    upper_bound = current_price + strikes_range

    filtered_puts = puts[(puts['strike'] >= lower_bound) & (puts['strike'] <= upper_bound)]

    return filtered_puts

# Usage example
expiration_date = '2024-04-12'
filtered_puts = get_amd_options(expiration_date)
if filtered_puts is not None:
    print(filtered_puts[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']])
