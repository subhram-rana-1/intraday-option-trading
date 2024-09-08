from trading.common.enums import StrategyType
from trading.common.exceptions import InvalidStrategyType
from trading.strategy.interface import IStrategy
from trading.strategy.long_momentum_call.long_momentum_call_startegy import LongMomentumCallStrategy
from trading.strategy.long_momentum_put.long_momentum_put_startegy import LongMomentumPutStrategy
from trading.strategy.short_strangle.short_strangle_startegy import ShortStrangleStrategy


def get_strategy(strategy_type: StrategyType) -> IStrategy:
    if strategy_type == StrategyType.LONG_MOMENTUM_CALL:
        return LongMomentumCallStrategy()
    elif strategy_type == StrategyType.LONG_MOMENTUM_PUT:
        return LongMomentumPutStrategy()
    elif strategy_type == StrategyType.SHORT_STRANGLE:
        return ShortStrangleStrategy()
    else:
        raise InvalidStrategyType(strategy_type)
