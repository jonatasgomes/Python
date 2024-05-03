import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def account_summary():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'portfolio/U14585657/summary'
    sum_req = requests.get(base_url + endpoint, verify=False)
    sum_json = json.dumps(sum_req.json(), indent=2)
    print(sum_req.status_code)
    print(sum_json)

if __name__ == '__main__':
    account_summary()
