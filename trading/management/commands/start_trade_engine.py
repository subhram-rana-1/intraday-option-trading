import threading
import time
from datetime import datetime
from django.core.management.base import BaseCommand

from trading.common.constants import market_start_time
from trading.common.entities.user_input import UserInput, StrategyInput
from trading.common.market_data import initialise_market_data_fetcher_client, MarketDataManager
from trading.strategy import get_strategy, IStrategy


def async_start_strategy(strategy_input: StrategyInput):
    strategy: IStrategy = get_strategy(strategy_input.strategy_type)

    thread = threading.Thread(target=lambda: strategy.start(
        strategy_input.trade_type,
        strategy_input.market,
        strategy_input.lot_qty,
    ))

    thread.start()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # initialise kite connect client as we will be using this for live market data fetch
        initialise_market_data_fetcher_client()

        # load NSE and NSO instrument data
        MarketDataManager.fetch_and_store_and_load_nse_nfo_instruments()

        # start fetch nifty and banknifty LTP
        MarketDataManager.start_async_fetching_nifty_and_banknifty_ltp()

        # wait till market opens
        while True:
            cur_time = datetime.now().time()
            if cur_time >= market_start_time:
                break
            else:
                time.sleep(3)

        # start async running strategies
        user_input: UserInput = UserInput.from_json_file()
        for strategy_input in user_input.strategy_inputs:
            async_start_strategy(strategy_input)
            time.sleep(0.2)
