from trading.common.enums import StrategyType
from trading.strategy.long_momentum.live_info import LongMomentumStrategyLiveInfo


class LongMomentumCallStrategyLiveInfo(LongMomentumStrategyLiveInfo):
    @property
    def strategy_type(self) -> StrategyType:
        return StrategyType.LONG_MOMENTUM_CALL
