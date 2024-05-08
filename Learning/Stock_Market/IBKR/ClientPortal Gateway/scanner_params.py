import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scan_params():
    base_url = 'https://localhost:5010/v1/api/'
    endpoint = 'iserver/scanner/params'
    params_req = requests.get(base_url + endpoint, verify=False)
    params_json = json.dumps(params_req.json(), indent=2)
    params_files = open('./scanner_params.xml', 'w')
    for i in params_json:
        params_files.write(i)
    params_files.close()
    print(params_req.status_code)

if __name__ == '__main__':
    scan_params()
