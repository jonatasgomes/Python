import api_sign
from datetime import datetime

def get_average_cost(asset_pair):
  data = api_sign.get_response("/0/private/TradesHistory").json()
  trades = data.get("result", {}).get("trades", {})
  trades = dict(sorted(trades.items(), key=lambda item: item[1]["time"])) # Sort by time
  
  total_cost = 0.0
  total_volume = 0.0
  for trade in trades.values():
    if trade["pair"] == asset_pair:
      trade_type = trade["type"]
      trade_date = datetime.fromtimestamp(trade["time"]).strftime("%Y-%m-%d %H:%M:%S")
      volume = float(trade["vol"])
      amt = float(trade["cost"]) +float(trade["fee"])
      price = float(trade["price"])
      if trade_type == "buy":
        total_cost += amt
      else:
        total_cost -= (total_cost / total_volume if total_volume > 0 else price) * volume
      total_volume += volume * (1 if trade_type == "buy" else -1)
      avg_price = total_cost / total_volume if total_volume > 0 else price
      print(f"Trade Date: {trade_date}, Trade Type: {trade_type}, Volume: {volume}, Price: {price:.2f} Amount: ${amt:.2f} Avg Price: ${avg_price:.2f}")

  return total_cost / total_volume if total_volume > 0 else 0.0, total_volume

avg_cost, balance = get_average_cost('SOLUSD')
print(f"Average cost: ${avg_cost:.2f}, Balance: {balance}")
