import requests
import env

BASE_URL = env.SANDBOX_BASE_URL
ACCESS_TOKEN = env.SANDBOX_ACCESS_TOKEN
ACCOUNT_ID = env.SANDBOX_ACCOUNT_ID

def make_request(endpoint, params=None, method='GET'):
    try:
        if method.upper() == 'GET':
            response = requests.get(
                BASE_URL + endpoint,
                params=params,
                headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"},
            )
        else:
            response = requests.post(
                BASE_URL + endpoint,
                data=params,
                headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"},
            )
        response.raise_for_status()
        json_response = response.json()
        print(response.status_code)
        print(json_response)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        print(f"Response content: {response.content if 'response' in locals() else 'No response'}")

if __name__ == "__main__":
    # make_request("/markets/quotes", {"symbols": "TSLA", "greeks": "false"})
    # make_request("/markets/options/chains", {"symbol": "TSLA", "expiration": "2025-12-19"})
    make_request(
        f"/accounts/{ACCOUNT_ID}/orders",
        {
            "class": "equity",
            "symbol": "TSLA",
            "side": "buy",
            "quantity": "1",
            "type": "market",
            "duration": "day",
        },
        "POST"
    )
    make_request(f"/accounts/{ACCOUNT_ID}/orders")
