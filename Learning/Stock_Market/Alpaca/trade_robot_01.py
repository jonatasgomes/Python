from alpaca.trading.client import *
import env

symbol = 'DELL'
client = TradingClient(api_key=env.API_KEY, secret_key=env.API_SECRET, paper=True)
try:
    position = client.get_open_position(symbol)
except:
    position = None

if position is not None:
    if float(position.qty_available) > 0.0:
        order = client.close_position(symbol)
        print(order)
    else:
        print(f'Qty available: {position.qty_available}')

orders = client.get_orders()
print(orders)
