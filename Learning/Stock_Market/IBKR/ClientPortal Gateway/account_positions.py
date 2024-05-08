import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def account_positions():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'portfolio/U14585657/positions/0'
    pos_req = requests.get(base_url + endpoint, verify=False)
    pos_json = json.dumps(pos_req.json(), indent=2)
    print(pos_req.status_code)
    print(pos_json)

if __name__ == '__main__':
    account_positions()
