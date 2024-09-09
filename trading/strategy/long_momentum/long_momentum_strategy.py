import time as tm
from trading.broker import BrokerCode, KiteBroker, UpstoxBroker, IBroker
from trading.common.constants import IST_timezone
from trading.common.entities.time_range import TimeRange
from django.db import transaction
from trading.common.entities.user_input import StrategyInput
from trading.common.enums import Market, StrategyType, TradeState, OrderPriceType, OrderStatus
from trading.common.market_data.instrument_data import InstrumentData
from trading.common.market_data.live_price_info import LivePriceInfo
from trading.common.utils import improvisation, get_quantity_from_lot_quantity
from trading.models import Trade, Order, Strategy
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

    @transaction.atomic
    def _buy(self):
        """
        TODO
        1. call broker Buy() function
        2. Save in 'trade' and 'order' DB table
        """
        current_market_price = self._get_market_price()
        root_stoploss = self._get_root_stoploss_from_market_price(current_market_price)
        instrument_symbol: str = self._get_instrument_symbol_from_market_price(current_market_price)
        instrument_token: int = InstrumentData.get_nfo_instrument_token_from_symbol(instrument_symbol)  # required when calling Buy() function

        self.broker.Buy()  # TODO: pass more details, not required for paper trading

        strategy: Strategy = Strategy.objects.get(name=self.strategy_type.value)
        trade: Trade = Trade(
            strategy=strategy,
            broker=self.strategy_input.broker_code,
            state=TradeState.IN_PROGRESS,
            day=datetime.today().day,
            initiation_time=datetime.now().astimezone(IST_timezone).time(),
            root_stoploss=root_stoploss,
        )
        trade.save()

        order: Order = Order(
            broker_txn_id='fake_txn_id',  # to fetch from Buy() function call
            trade=trade,
            txn_type='BUY',
            instrument_symbol=instrument_symbol,
            qty=get_quantity_from_lot_quantity(self.strategy_input.market, self.strategy_input.lot_qty),
            price_type=OrderPriceType.MARKET,
            status=OrderStatus.CONFIRMED,  # TODO: to get it from Buy() api call
            order_request_time='',
            order_request_price='',
            order_confirmation_time='',
            order_confirmation_price='',
            tot_amount='',
        )
        order.save()

    def _sell(self):
        """
        TODO
        1. call broker Sell() function
        2. Save in 'order' DB table
        """

    def _get_market_price(self) -> float:
        market: Market = self.strategy_input.market

        if market == Market.NIFTY:
            return LivePriceInfo.nifty['last_price']
        elif market == Market.NIFTY:
            return LivePriceInfo.banknifty['last_price']

        raise Exception(f'invalid market type: {market.value}')

    def _get_root_stoploss_from_market_price(self, market_price: float) -> float:
        return market_price - self.strategy_config.root_sl_deviation_pt

    @abstractmethod
    def _get_instrument_symbol_from_market_price(self, current_market_price: float) -> str:
        ...
