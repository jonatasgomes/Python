import api_sign

print(api_sign.get_response("/0/private/AddOrder", { "ordertype": "limit", "type": "buy", "volume": "0.13294117", "pair": "SOLUSD", "price": "256" }).text)
