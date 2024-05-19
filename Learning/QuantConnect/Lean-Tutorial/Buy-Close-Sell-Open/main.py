# region imports
from AlgorithmImports import *
# endregion

class BuyCloseSellOpen(QCAlgorithm):

    def __init__(self):
        super().__init__()
        self.closing_order_sent = None
        self.security = None

    def initialize(self):
        # Locally Lean installs free sample data, to download more data please visit
        # https://www.quantconnect.com/docs/v2/lean-cli/datasets/downloading-data
        self.set_start_date(2002, 8, 1)  # Set Start Date
        self.set_end_date(2022, 8, 5)  # Set End Date
        self.set_cash(1000000)  # Set Strategy Cash
        self.security = self.add_equity("SPY", Resolution.MINUTE)
        self.set_brokerage_model(BrokerageName.INTERACTIVE_BROKERS_BROKERAGE, AccountType.MARGIN)
        self.security.set_fee_model(ConstantFeeModel(0))
        self.set_benchmark(self.security.type, self.security.symbol)
        self.schedule.on(
            self.date_rules.every_day(),
            self.time_rules.after_market_open(self.security.symbol, 1),
            self.sell_open
        )

    def on_data(self, data: Slice):
        if self.time.hour == 15 and self.time.minute == 59:
            self.set_holdings(self.security.symbol, 1)

    def sell_open(self):
        if self.portfolio.invested:
            self.set_holdings(self.security.symbol, 0)
