from trading.broker.enums import BrokerCode
from trading.broker.exceptions import InvalidBrokerException
from trading.broker.interface import IBroker
from trading.broker.kite.broker import KiteBroker
from trading.broker.simulator.broker import BrokerSimulator
from trading.broker.upstox.broker import UpstoxBroker


def new_broker(broker_code: BrokerCode) -> IBroker:
    if broker_code == BrokerCode.KITE:
        return KiteBroker()
    if broker_code == BrokerCode.UPSTOX:
        return UpstoxBroker()
    if broker_code == BrokerCode.SIMULATOR:
        return BrokerSimulator()

    raise InvalidBrokerException(f'broker code: {broker_code}')
