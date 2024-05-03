# https://algotrading101.com/learn/ib_insync-interactive-brokers-api-guide/
# https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/#what-is-ib-python-api-native
# https://github.com/topics/interactive-brokers?l=python
# https://ibkrcampus.com/trading-lessons/placing-orders/

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def confirmStatus():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'iserver/auth/status'
    auth_req = requests.get(base_url + endpoint, verify=False)
    print(auth_req)
    print(auth_req.text)

if __name__ == '__main__':
    confirmStatus()
