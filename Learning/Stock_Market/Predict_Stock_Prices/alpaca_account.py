from alpaca.trading.client import *
import env

client = TradingClient(api_key=env.API_KEY, secret_key=env.API_SECRET, paper=True, url_override=None)
account = client.get_account()
print(account)
