import time as tm
from trading.common.entities.time_range import TimeRange
from trading.common.enums import TradeType, Market, StrategyType, TradeState
from trading.models import Trade, Order
from trading.strategy import IStrategy
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, time

from trading.strategy.long_momentum.strategy_config import LongMomentumStrategyConfig


class LongMomentumStrategy(IStrategy, ABC):
    @property
    @abstractmethod
    def strategy_type(self) -> StrategyType:
        ...

    @property
    def config(self) -> LongMomentumStrategyConfig:
        return LongMomentumStrategyConfig()

    def start(self, trade_type: TradeType, market: Market, lot_qty: int):
        while True:
            cur_time: time = datetime.now().time()
            trade: Trade = self._get_latest_trade_for_this_strategy()

            if trade is None or trade.state == TradeState.COMPLETED:
                if cur_time > self.config.max_square_off_time:
                    print(f'STOPPING {self.strategy_type} strategy for today as'
                          f'we exceeded max square off time')
                    break

                """Need to take a new trade"""
                self._try_buying()

            elif trade.state == TradeState.IN_PROGRESS:
                """Need to square off the ongoing trade"""
                self._try_selling()

            tm.sleep(1)

    @classmethod
    def _get_latest_trade_for_this_strategy(cls) -> Trade:
        try:
            latest_trade: Trade = Trade.objects.latest('id')
        except Trade.DoesNotExist:
            latest_trade = None

        return latest_trade

    def _try_buying(self) -> Trade:
        """TODO"""

    def _try_selling(self) -> Trade:
        """TODO"""
