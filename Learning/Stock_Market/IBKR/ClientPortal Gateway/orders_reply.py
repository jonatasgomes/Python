import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def order_request():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'iserver/reply/eb795e99-f2b9-450e-97f1-176ef1da0060'
    json_body = {
        'confirmed': True
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
