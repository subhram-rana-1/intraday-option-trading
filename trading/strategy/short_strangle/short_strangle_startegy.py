from trading.common.enums import Market
from trading.strategy import IStrategy


class ShortStrangleStrategy(IStrategy):
    def start(self, market: Market, lot_qty: int):
        raise NotImplemented
