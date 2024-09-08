from trading.common.enums import TradeType, Market
from trading.strategy import IStrategy
from trading.strategy.long_momentum.long_momentum_strategy import LongMomentumStrategy


class LongMomentumPutStrategy(IStrategy, LongMomentumStrategy):
    def start(self, trade_type: TradeType, market: Market, lot_qty: int):
        raise NotImplemented
