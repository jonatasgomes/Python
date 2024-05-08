from ibapi.client import *
from ibapi.wrapper import *
import time


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def contractDetails(self, reqId, contractDetails):
        print(f"Contract Details: {contractDetails}")

    def contractDetailsEnd(self, reqId: int):
        print(f"Contract Details End: {reqId}")
        self.disconnect()


def main():
    app = TestApp()
    app.connect('127.0.0.1', 4002, 1000)
    mycontract = Contract()
    mycontract.conId = 265598
    # mycontract.symbol = 'AAPL'
    # mycontract.secType = 'STK'
    # mycontract.exchange = 'SMART'
    # mycontract.currency = 'USD'
    # mycontract.primaryExchange = 'ISLAND'
    time.sleep(1)
    app.reqContractDetails(1, mycontract)
    app.run()


if __name__ == '__main__':
    main()

# https://ibkrcampus.com/ibkr-api-page/twsapi-doc/#The-IB-Gateway
# https://interactivebrokers.github.io/tws-api/connection.html
