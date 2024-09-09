import time as tm

from trading.broker import BrokerCode, KiteBroker, UpstoxBroker, IBroker
from trading.common.entities.time_range import TimeRange
from trading.common.entities.user_input import StrategyInput
from trading.common.enums import Market, StrategyType, TradeState
from trading.common.utils import improvisation
from trading.models import Trade, Order
from trading.strategy import IStrategy
from abc import ABC, abstractmethod
from datetime import datetime, time
from trading.strategy.long_momentum.live_info import LongMomentumStrategyLiveInfo
from trading.strategy.long_momentum.strategy_config import LongMomentumStrategyConfig


class LongMomentumStrategy(IStrategy, ABC):
    @abstractmethod
    def __init__(
            self,
            strategy_user_input: StrategyInput,
            strategy_config: LongMomentumStrategyConfig,
    ):
        self.strategy_input: StrategyInput = strategy_user_input
        self.strategy_config: LongMomentumStrategyConfig = strategy_config
        self.broker: IBroker = None
        self.live_info: LongMomentumStrategyLiveInfo = None

        raise Exception("can't instantiate LongMomentumStrategy abstract class."
                        "You must need to instantiate the inherited ones.")

    @property
    @abstractmethod
    def strategy_type(self) -> StrategyType:
        ...

    def start(self, market: Market, lot_qty: int):
        while True:
            cur_time: time = datetime.now().time()
            trade: Trade = self._get_latest_trade_for_this_strategy()

            if trade is None or trade.state == TradeState.COMPLETED:
                if cur_time > self.strategy_config.max_square_off_time:
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

    def _try_buying(self):
        while True:
            cur_time = datetime.now().time()

            if cur_time > self.strategy_config.max_square_off_time:
                return

            if not self.is_suitable_buying_time(cur_time):
                tm.sleep(60)  # wait 1 min
                continue

            # This is a suitable buying time, so try looking for momentum
            if self._is_entry_possible():
                self._buy()
                return
            else:
                tm.sleep(1)
                continue

    def _try_selling(self):
        while True:
            cur_time = datetime.now().time()

            if cur_time > self.strategy_config.max_square_off_time:
                self._sell()
                return

            if self.is_SL_hit():
                self._sell()
                return

            # else train the SL
            self._trail_SL()

            tm.sleep(1)

    def is_suitable_buying_time(self, cur_time: time) -> bool:
        for tr in self.strategy_config.allowed_time_ranges_for_entry:
            if tr.start <= cur_time <= tr.end:
                return True

        return False

    @abstractmethod
    def _is_entry_possible(self) -> bool:
        ...

    def is_SL_hit(self) -> bool:
        if self.live_info.option_ltp <= self.live_info.root_stoploss:
            return True

        if self.live_info.cur_stoploss is not None and \
                self.live_info.option_ltp <= self.live_info.cur_stoploss:
            return True

        return False

    @improvisation('while setting up first self.live_info.cur_stoploss')
    def _trail_SL(self):
        if self.live_info.cur_stoploss is not None:
            # try to trail the SL
            new_stoploss = self.live_info.option_ltp - self.strategy_config.max_allowed_price_fluctuation_pt
            self.live_info.cur_stoploss = max(self.live_info.cur_stoploss, new_stoploss)
        else:
            # Try to initialise cur_stoploss is possible
            if self.live_info.option_ltp >= \
                    self.live_info.buying_price + self.strategy_config.min_profit_pt + \
                    self.strategy_config.max_allowed_price_fluctuation_pt:
                self.live_info.cur_stoploss = \
                    self.live_info.option_ltp - self.strategy_config.max_allowed_price_fluctuation_pt

    def _buy(self):
        """
        TODO
        1. call broker Buy() function
        2. Save in 'trade' and 'order' DB table
        """

    def _sell(self):
        """
        TODO
        1. call broker Sell() function
        2. Save in 'order' DB table
        """