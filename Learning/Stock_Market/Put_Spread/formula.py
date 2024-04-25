import pandas as pd
import yfinance as yf

def get_amd_options(expiration_date, strikes_range=10):
    # Fetch AMD stock data
    amd_stock = yf.Ticker("DELL")

    # Get the current stock price using .iloc for positional indexing
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
    lower_bound = current_price #- strikes_range
    upper_bound = current_price + strikes_range

    filtered_puts = puts[(puts['strike'] >= lower_bound) & (puts['strike'] <= upper_bound)]

    # Initialize a list to store the results
    results = []

    # Loop through the filtered put options to compute the specified formula
    for i in range(len(filtered_puts)):
        for j in range(i + 1, len(filtered_puts)):
            strike_i = filtered_puts.iloc[i]['strike']
            price_i = filtered_puts.iloc[i]['lastPrice']

            strike_j = filtered_puts.iloc[j]['strike']
            price_j = filtered_puts.iloc[j]['lastPrice']

            # Compute the formula
            formula_result = (strike_i - strike_j) - (price_i - price_j)

            # Store the result
            results.append({
                'strike[i]': strike_i,
                'strike[j]': strike_j,
                'formula_result': formula_result
            })

    # Convert the results to a DataFrame for better visualization
    results_df = pd.DataFrame(results)
    return results_df

# Usage example
expiration_date = '2024-04-12'
formula_results = get_amd_options(expiration_date)
if formula_results is not None:
    print(formula_results)
