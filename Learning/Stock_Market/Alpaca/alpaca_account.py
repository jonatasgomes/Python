from alpaca.trading import QueryOrderStatus
from alpaca.trading.client import *
import env

client = TradingClient(api_key=env.API_KEY, secret_key=env.API_SECRET, paper=True, url_override=None)
account = client.get_account().cash
print(account)

get_orders_data = GetOrdersRequest(
    status=QueryOrderStatus.ALL,
    limit=100,
    nested=True  # show nested multi-leg orders
)

orders = client.get_orders(filter=get_orders_data)
[print(f'{order.symbol}, {order.qty}, {order.filled_qty}, {order.status}') for order in orders]
