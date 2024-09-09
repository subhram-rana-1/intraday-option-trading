import threading
from datetime import datetime, date
from abc import ABC, abstractmethod
from kiteconnect import KiteTicker
import time as tm
from trading.broker.kite.utils import new_kite_websocket_client
from trading.common.enums import StrategyType, TradeState
from trading.common.market_data.instrument_data import InstrumentData
from trading.common.market_data.ticker_data import TickerData
from trading.models import Trade, Strategy, Order


class LongMomentumStrategyLiveInfo(ABC):
    def __init__(self):
        """
        TODO
        Try to load 'trade' and 'order' from DB, if not exists initiate with default values
        else load 'root_stoploss' and 'buying_price'
        """
        today: date = datetime.today().date()
        strategy: Strategy = Strategy.objects.get(name=self.strategy_type.value)

        try:
            trade: Trade = Trade.objects.filter(strategy=strategy, day=today).first()
        except Trade.DoesNotExist:
            self.root_stoploss: float = None  # static, only will be set while buying
            self.buying_price: float = None  # static, only will be set while buying
            self.option_symbol: str = None  # static, only will be set while buying
            self.option_instrument_token: int = None  # static, only will be set while buying
            self.option_ltp: float = None  # updated on every seconds in 'async_start_fetching_option_ltp()' function
            self.cur_stoploss: float = None  # updated in every 1 second after in
            # 'LongMomentumStrategy._try_selling()' function
        else:
            if trade.state == TradeState.COMPLETED:
                self.root_stoploss: float = None
                self.buying_price: float = None
                self.option_symbol: str = None
                self.option_instrument_token: int = None
                self.option_ltp: float = None
                self.cur_stoploss: float = None
            elif trade.state == TradeState.IN_PROGRESS:
                order: Order = Order.objects.filter(trade=trade).first()

                self.root_stoploss: float = trade.root_stoploss
                self.buying_price: float = order.order_confirmation_price
                self.option_symbol: str = order.instrument_symbol
                self.option_instrument_token = InstrumentData.get_nfo_instrument_token_from_symbol(order.instrument_symbol)
                self.option_ltp = None
                self.cur_stoploss = None

    def save_buying_info_in_database(
            self,
            option_symbol: str,
            option_instrument_token: str,
            buying_price: float,
            root_stoploss: float,
    ):
        """
        1. Set root_stoploss, buying_price once
        2. Create DB records in 'trade' and 'order" table
        3. spawn async_start_fetching_option_ltp() function
        """
        self.root_stoploss = root_stoploss
        self.buying_price = buying_price
        self.option_symbol = option_symbol
        self.option_instrument_token = option_instrument_token

        # TODO: create DB records

        self.async_start_fetching_option_ltp()

    def save_selling_info_in_database(self):
        """
        TODO
        1. Create DB records in 'order" table
        """

    @abstractmethod
    @property
    def strategy_type(self) -> StrategyType:
        ...

    def async_start_fetching_option_ltp(self):
        try:
            trade: Trade = Trade.objects.get()  # TODO: fetch the trade from DB
        except Trade.DoesNotExist:
            return
        else:
            if trade.state == TradeState.COMPLETED:
                return
            if trade.state == TradeState.IN_PROGRESS:
                # async keep on fetching option ltp
                thread = threading.Thread(target=self.start_fetching_option_ltp)
                thread.start()

    def start_fetching_option_ltp(self):
        kws: KiteTicker = new_kite_websocket_client()

        kws.on_connect = self.subscribe_to_option_instrument
        kws.on_ticks = self.update_option_ltp
        kws.on_close = self.close_websocket_connection

        kws.connect(threaded=True)

        today: date = datetime.today().date()
        strategy: Strategy = Strategy.objects.get(name=self.strategy_type.value)
        while True:
            trade = Trade.objects.filter(strategy=strategy, day=today).first()
            if trade.state == TradeState.COMPLETED:
                break
            else:
                tm.sleep(60)

        kws.close()

    def subscribe_to_option_instrument(self, ws, response):
        option_instrument_token = self.option_instrument_token

        ws.subscribe([option_instrument_token])
        ws.set_mode(ws.MODE_LTP, [option_instrument_token])

    def update_option_ltp(self, ws, ticks):
        stock_data: TickerData = ticks[0]
        self.option_ltp = stock_data['last_price']

    @staticmethod
    def close_websocket_connection(ws, code, reason):
        ws.stop()
