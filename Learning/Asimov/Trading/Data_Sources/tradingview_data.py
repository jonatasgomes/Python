import requests
import env

username = env.TV_USER
password = env.TV_PWD
requests.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
response = requests.post(
   url='https://www.tradingview.com/accounts/signin/',
   data={
       "username": username,
       "password": password,
       "remember": "on",
   },
   headers={'Referer': 'https://www.tradingview.com'},
)
print(response.json())
