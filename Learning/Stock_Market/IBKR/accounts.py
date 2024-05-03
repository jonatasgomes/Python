import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def req_accounts():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'iserver/accounts'
    accts_req = requests.get(base_url + endpoint, verify=False)
    print(accts_req)
    try:
        accts_json = json.dumps(accts_req.json(), indent=2)
        print(accts_json)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    req_accounts()
