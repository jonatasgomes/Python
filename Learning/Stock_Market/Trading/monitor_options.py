import yfinance as yf

def monitor_spy_options(expiration_date):
    # Download the SPY ticker
    spy = yf.Ticker("^SPX")

    # Fetch the option chain for the specified expiration date
    try:
        options = spy.option_chain(expiration_date)
        calls = options.calls
        puts = options.puts

        # Display the calls and puts in the options chain
        print("Call Options:")
        print(calls[['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']].sort_values(by='openInterest', ascending=False).head(10))

        print("\nPut Options:")
        print(puts[['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']].sort_values(by='openInterest', ascending=False).head(10))

    except Exception as e:
        print(f"Error fetching options data: {e}")

# Example usage
monitor_spy_options("2025-03-21")  # Specify the desired expiration date
