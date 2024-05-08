import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def iserver_scanner():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'iserver/scanner/run'
    scan_body = {
        'instrument': 'STK',
        'location': 'STK.US.MAJOR',
        'type': 'TOP_PERC_GAIN',
        'filter': [
            {
                'code': 'priceAbove',
                'value': 184
            },
            {
                'code': 'priceBelow',
                'value': 186
            }
        ]
    }
    scan_req = requests.post(base_url + endpoint, verify=False, json=scan_body)
    scan_json = json.dumps(scan_req.json(), indent=2)
    print(scan_req.status_code)
    print(scan_json)

if __name__ == '__main__':
    iserver_scanner()
