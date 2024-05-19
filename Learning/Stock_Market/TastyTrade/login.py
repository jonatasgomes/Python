from tastytrade_sdk import Tastytrade
import env

tasty = Tastytrade(api_base_url='api.cert.tastyworks.com')
tasty.login(
    login=env.USER,
    password=env.PWD
)
tasty.api.post('/sessions/validate')
resp = tasty.api.get(
    '/api-quote-tokens'
)
print(resp)
tasty.logout()
