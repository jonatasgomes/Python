from tastytrade_sdk import Tastytrade
import env

tasty = Tastytrade()
tasty.login(
    login=env.USER,
    password=env.PWD
)
tasty.api.post('/sessions/validate')
tasty.logout()
