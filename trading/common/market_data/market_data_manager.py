import threading
import time
import json
from datetime import date, datetime
from kiteconnect import KiteConnect, KiteTicker
from abc import ABC, abstractmethod

from trading.broker.kite.utils import new_kite_websocket_client
from trading.common.constants import market_start_time, market_end_time, trading_symbol_nifty_50, \
    trading_symbol_banknifty
from trading.common.market_data.constants import nse_data_relative_path, nfo_data_relative_path
from trading.common.market_data.instrument_data import InstrumentData
from trading.common.market_data.live_price_info import LivePriceInfo
from trading.common.market_data.ticker_data import TickerData


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()  # Convert date and datetime to string
        return super().default(obj)


class DataManager(ABC):
    @property
    @abstractmethod
    def exchange(self) -> str:
        ...

    @property
    @abstractmethod
    def data_relative_path(self) -> str:
        ...

    def __init__(self, kc: KiteConnect):
        self.kc: KiteConnect = kc

    def fetch_and_store_and_load_instruments(self):
        instruments: dict = self._fetch_instruments()
        self._save_instruments(instruments)
        self.load_instruments()

    def _fetch_instruments(self) -> dict:
        all_instruments = self.kc.instruments(self.exchange)

        all_data = {}
        for data in all_instruments:
            all_data[f'{data['tradingsymbol']}'] = data

        return all_data

    def _save_instruments(self, instruments: dict):
        with open(self.data_relative_path, 'w') as json_file:
            json.dump(instruments, json_file, indent=4)

    def load_instruments(self):
        with open(self.data_relative_path, 'r') as file:
            data_dict = json.load(file)

        if self.exchange == self.kc.EXCHANGE_NSE:
            InstrumentData.nse_instruments = data_dict
        elif self.exchange == self.kc.EXCHANGE_NFO:
            InstrumentData.nfo_instruments = data_dict


class NSEDataManager(DataManager):

    @property
    def exchange(self) -> str:
        return self.kc.EXCHANGE_NSE

    @property
    def data_relative_path(self) -> str:
        return nse_data_relative_path


class NFODataManager(DataManager):

    @property
    def exchange(self) -> str:
        return self.kc.EXCHANGE_NFO

    @property
    def data_relative_path(self) -> str:
        return nfo_data_relative_path


class MarketDataManager:
    kc: KiteConnect = None
    nse_data_manager = None
    nfo_data_manager = None
    live_price_info: LivePriceInfo = LivePriceInfo()

    @classmethod
    def bootstrap(cls, kc: KiteConnect):
        cls.kc = kc
        cls.nse_data_manager: NSEDataManager = NSEDataManager(kc)
        cls.nfo_data_manager: NFODataManager = NFODataManager(kc)

    @classmethod
    def fetch_and_store_and_load_nse_nfo_instruments(cls):
        cls.nse_data_manager.fetch_and_store_and_load_instruments()
        cls.nfo_data_manager.fetch_and_store_and_load_instruments()

    @classmethod
    def start_async_fetching_nifty_and_banknifty_ltp(cls):
        # wait for market to start
        while True:
            cur_time = datetime.now().time()
            if cur_time >= market_start_time:
                break

            time.sleep(3)

        cls._async_start_async_fetching_nifty_ltp()
        cls._async_start_async_fetching_banknifty_ltp()

    @classmethod
    def _async_start_async_fetching_nifty_ltp(cls):
        thread = threading.Thread(target=start_fetching_and_updating_nifty_price)
        thread.start()

    @classmethod
    def _async_start_async_fetching_banknifty_ltp(cls):
        thread = threading.Thread(target=start_fetching_and_updating_banknifty_price)
        thread.start()


def start_fetching_and_updating_nifty_price():
    kws: KiteTicker = new_kite_websocket_client()

    kws.on_connect = subscribe_to_nifty_instrument
    kws.on_ticks = update_nifty_ltp
    kws.on_close = close_websocket_connection

    kws.connect(threaded=True)

    while True:
        cur_time = datetime.now().time()
        if cur_time >= market_end_time:
            break
        else:
            time.sleep(60)

    kws.close()


def subscribe_to_nifty_instrument(ws, response):
    nifty_50_instrument_token = InstrumentData.nse_instruments[trading_symbol_nifty_50]['instrument_token']
    ws.subscribe([nifty_50_instrument_token])
    ws.set_mode(ws.MODE_LTP, [nifty_50_instrument_token])


def update_nifty_ltp(ws, ticks):
    stock_data: TickerData = ticks[0]
    MarketDataManager.live_price_info.nifty['last_price'] = stock_data['last_price']


def start_fetching_and_updating_banknifty_price():
    kws: KiteTicker = new_kite_websocket_client()

    kws.on_connect = subscribe_to_banknifty_instrument
    kws.on_ticks = update_banknifty_ltp
    kws.on_close = close_websocket_connection

    kws.connect(threaded=True)

    while True:
        cur_time = datetime.now().time()
        if cur_time >= market_end_time:
            break
        else:
            time.sleep(60)

    kws.close()


def subscribe_to_banknifty_instrument(ws, response):
    banknifty_instrument_token = InstrumentData.nse_instruments[trading_symbol_banknifty]['instrument_token']
    ws.subscribe([banknifty_instrument_token])
    ws.set_mode(ws.MODE_LTP, [banknifty_instrument_token])


def update_banknifty_ltp(ws, ticks):
    stock_data: TickerData = ticks[0]
    MarketDataManager.live_price_info.banknifty['last_price'] = stock_data['last_price']


def close_websocket_connection(ws, code, reason):
    ws.stop()


