from trading.common.market_data.ticker_data import TickerData


class LivePriceInfo:
    nifty: TickerData = None
    banknifty: TickerData = None
    option_prices: dict = {}  # map(option instrument symbol --> ticker data)
