from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass
import env

trading_client = TradingClient(env.API_KEY, env.API_SECRET, paper=True)

# preparing bracket order with both stop loss and take profit
bracket__order_data = MarketOrderRequest(
    symbol="GOOG",
    qty=5,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY,
    order_class=OrderClass.BRACKET,
    take_profit=TakeProfitRequest(limit_price=200),
    stop_loss=StopLossRequest(stop_price=150)
)

bracket_order = trading_client.submit_order(
    order_data=bracket__order_data
)

# preparing oto order with stop loss
oto_order_data = LimitOrderRequest(
    symbol="GOOG",
    qty=5,
    limit_price=175,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY,
    order_class=OrderClass.OTO,
    stop_loss=StopLossRequest(stop_price=150)
)

# Market order
oto_order = trading_client.submit_order(
    order_data=oto_order_data
)
