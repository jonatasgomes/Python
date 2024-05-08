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
        self.reqMarketDataType(4)
        self.reqMktData(orderId, mycontract, '', False, False, [])

    def tickPrice(self, reqId:TickerId , tickType:TickType, price:float,
                  attrib:TickAttrib):
        print(f'tickPrice reqId: {reqId} tickType: {TickTypeEnum.to_str(tickType)} price: {price} attribs: {attrib}')

    def tickSize(self, reqId:TickerId, tickType:TickType, size:int):
        print(f'tickSize reqId: {reqId} tickType: {TickTypeEnum.to_str(tickType)} size: {size}')


app = TestApp()
app.connect('127.0.0.1', 4002, clientId=1000)
app.run()
