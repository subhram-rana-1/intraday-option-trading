from abc import ABC, abstractmethod
from trading.common.enums import Market


class IStrategy(ABC):
    @abstractmethod
    def start(
            self,
            market: Market,
            lot_qty: int,
    ):
        raise NotImplemented
