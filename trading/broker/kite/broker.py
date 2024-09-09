from trading.broker import IBroker
from trading.common.market_data import kite_connect_client


class KiteBroker(IBroker):
    def __init__(self):
        self.kc = kite_connect_client

    def Buy(self):
        pass

    def Sell(self):
        pass
