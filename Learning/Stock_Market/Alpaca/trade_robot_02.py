from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.stream import TradingStream
import env

trading_client = TradingClient(env.API_KEY, env.API_SECRET, paper=True)
stream = TradingStream(env.API_KEY, env.API_SECRET, paper=True)
client_order_id = 'jga_my_order_01'

order_data = MarketOrderRequest(
    symbol="BAC",
    qty=1,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.GTC,
    trail_percent=1.00,
    client_order_id=client_order_id
)

order = trading_client.submit_order(
    order_data=order_data
)

@stream.on(client_order_id)
async def on_msg(data):
    # Print the update to the console.
    print("Update for {}. Event: {}.".format(data.event, data.data))

stream.subscribe_trade_updates(on_msg)
stream.run()
