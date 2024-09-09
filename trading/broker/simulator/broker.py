from trading.broker import IBroker


class BrokerSimulator(IBroker):
    def Buy(self):
        print('fake buying...')
        pass

    def Sell(self):
        print('fake selling...')
        pass
