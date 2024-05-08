from tastytrade_sdk import Tastytrade
import env

tasty = Tastytrade(api_base_url='api.cert.tastyworks.com')
tasty.login(login=env.USER, password=env.PWD)
symbols = [
    'BTC/USD',
    'SPY',
    '/ESU3',
    'SPY   230630C00255000',
    './ESU3 EW2N3 230714C4310'
]
subscription = tasty.market_data.subscribe(
    symbols=symbols,
    on_quote=print,
    on_candle=print,
    on_greeks=print
)
# subscription.__url = 'streamer.cert.tastyworks.com'
subscription.open()
