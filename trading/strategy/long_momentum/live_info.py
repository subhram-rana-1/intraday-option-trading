from trading.strategy.long_momentum.strategy_config import LongMomentumStrategyConfig


class LongMomentumStrategyLiveInfo:
    def __init__(self, strategy_config: LongMomentumStrategyConfig):
        self.option_instrument_symbol: str = None
        self.option_ltp: float = None
        self.root_stoploss: float = None
        self.cur_stoploss: float = None
        self.config = strategy_config

