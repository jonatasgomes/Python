from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        mycontract = Contract()
        # mycontract.conId = 265598
        mycontract.symbol = 'AAPL'
        mycontract.secType = 'STK'
        mycontract.exchange = 'SMART'
        mycontract.currency = 'USD'
        self.reqHistoricalData(orderId, mycontract, '20240503 10:00:00 US/Eastern', '1 D',
                               '1 hour', 'TRADES', 0, 1,
                               False, [])

    def historicalData(self, reqId, bar):
        print(f'Historical Data: {bar}')

    def historicalDataEnd(self, reqId, start, end):
        print(f'End of Historical Data: start {start}, end {end}')


app = TestApp()
app.connect('127.0.0.1', 4001, clientId=1000)
app.run()
