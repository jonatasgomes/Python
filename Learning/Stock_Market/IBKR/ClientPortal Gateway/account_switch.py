import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def req_accounts():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'iserver/account'
    acct_body = {
        'acctId': 'U14570444'  # 'U14570444'
    }
    acct_req = requests.post(base_url + endpoint, verify=False, json=acct_body)
    print(acct_req.text)
    if acct_req.status_code in (200, 400):
        acct_json = json.dumps(acct_req.json(), indent=2)
        print(acct_json)

if __name__ == '__main__':
    req_accounts()
