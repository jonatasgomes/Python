import json
import urllib.parse
import hashlib
import hmac
import base64
import env
import time
import requests

def get_nonce():
  return str(int(time.time()*1000))

def set_signature(_payload=None):
    global headers, payload, url_path
    payload = json.dumps({"nonce": get_nonce(), **(_payload or {})})
    if isinstance(payload, str):
        encoded = (str(json.loads(payload)["nonce"]) + payload).encode()
    else:
        encoded = (str(payload["nonce"]) + urllib.parse.urlencode(payload)).encode()
    message = url_path.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(env.PRIVATE_KEY), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest()).decode()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'API-Key': env.API_KEY,
        'API-Sign': sigdigest
    }

def get_response(_path, _payload=None):
    global url_path
    url_path = _path
    set_signature(_payload)
    return requests.request("POST", url_base + url_path, headers=headers, data=payload)

url_base = "https://api.kraken.com"
url_path = None
headers = {}
payload = None
