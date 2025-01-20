import requests
from datetime import datetime, timezone

url = "https://api.kraken.com/0/public/Trades?pair=SOLUSD&count=5"

payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()

if data["error"]:
  print("Error:", data["error"])
else:
  trades = data["result"]["SOLUSD"]
  for trade in trades:
    price, volume, time, side, order_type, misc, trade_id = trade
    trade_time = datetime.fromtimestamp(time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Price: {price}, Volume: {volume}, Time: {trade_time}, Side: {side}, Order Type: {order_type}, Trade ID: {trade_id}")
