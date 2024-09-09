from trading.common.enums import Market
from trading.strategy import IStrategy
from trading.strategy.long_momentum.long_momentum_strategy import LongMomentumStrategy


class LongMomentumPutStrategy(IStrategy, LongMomentumStrategy):
    def start(self, market: Market, lot_qty: int):
        raise NotImplemented
