from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        self.reqScannerParameters()

    def scannerParameters(self, xml):
        _dir = './scanner_params.xml'
        open(_dir, 'w').write(xml)
        print('Scanner params file received.')

app = TestApp()
app.connect('127.0.0.1', 4002, clientId=1000)
app.run()
