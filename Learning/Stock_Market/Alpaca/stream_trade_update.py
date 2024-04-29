from alpaca.trading.stream import TradingStream
import env

# subscribe trade updates
trade_stream_client = TradingStream(env.API_KEY, env.API_SECRET, paper=True)

async def trade_updates_handler(data):
    print(data)

trade_stream_client.subscribe_trade_updates(trade_updates_handler)
trade_stream_client.run()
