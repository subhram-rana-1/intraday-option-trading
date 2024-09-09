from trading.broker import BrokerCode, IBroker, KiteBroker, UpstoxBroker, new_broker
from trading.common.entities.user_input import StrategyInput
from trading.common.enums import StrategyType
from trading.common.utils import improvisation
from trading.strategy.long_momentum.exceptions import InvalidBrokerCodeToInitialiseStrategyException
from trading.strategy.long_momentum.long_momentum_strategy import LongMomentumStrategy
from trading.strategy.long_momentum_call.live_info import LongMomentumCallStrategyLiveInfo
from trading.strategy.long_momentum_call.strategy_config import LongMomentumCallStrategyConfig


class LongMomentumCallStrategy(LongMomentumStrategy):
    def __init__(
            self,
            strategy_user_input: StrategyInput,
            strategy_config: LongMomentumCallStrategyConfig,
    ):
        if strategy_user_input.strategy_type != StrategyType.LONG_MOMENTUM_CALL:
            raise Exception(f'strategy type validation failed for'
                            f' long momentum call strategy: {strategy_user_input.strategy_type.value}')

        self.strategy_input: StrategyInput = strategy_user_input
        self.strategy_config: LongMomentumCallStrategyConfig = strategy_config
        self.broker: IBroker = new_broker(strategy_user_input.broker_code)
        self.live_info: LongMomentumCallStrategyLiveInfo = LongMomentumCallStrategyLiveInfo()
        self.live_info.async_start_fetching_option_ltp()

    @property
    def strategy_type(self) -> StrategyType:
        return StrategyType.LONG_MOMENTUM_CALL

    @improvisation("necessary technical analysis should be done")
    def _is_entry_possible(self) -> bool:
        """TODO: implement entry algorithm"""
        return True
