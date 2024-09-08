from abc import ABC, abstractmethod
from trading.common.enums import TradeType, Market


class IStrategy(ABC):
    @abstractmethod
    def start(
            self,
            trade_type: TradeType,
            market: Market,
            lot_qty: int,
    ):
        raise NotImplemented
