import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def order_request():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'iserver/account/U14570444/orders'
    json_body = {
        "orders": [{
            "conid": 265598,
            "orderType": "STP",
            "price": 190,
            "side": "BUY",
            "tif": "DAY",
            "quantity": 1
        }]
    }
    order_req = requests.post(base_url + endpoint, verify=False, json=json_body)
    print(order_req.status_code)
    try:
        order_json = json.dumps(order_req.json(), indent=2)
        print(order_json)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    order_request()
