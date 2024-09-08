import json
from typing import List
from trading.common.constants import user_input_json_file_relative_path
from trading.common.enums import StrategyType, TradeType, Market


class StrategyInput:
    def __init__(
            self,
            strategy_type: str,
            should_run: bool,
            trade_type: str,
            market: str,
            lot_qty: int,
    ):
        self.strategy_type = StrategyType(strategy_type)
        self.should_run = should_run
        self.trade_type = TradeType(trade_type)
        self.market = Market(market)
        self.lot_qty = lot_qty


class UserInput:

    def __init__(self):
        self.strategy_inputs: List[StrategyInput] = []

    def _append_strategy_input(self, strategy_input: StrategyInput):
        self.strategy_inputs.append(strategy_input)

    @classmethod
    def from_json_file(cls):
        with open(user_input_json_file_relative_path, 'r') as user_input_file:
            data: dict = json.load(user_input_file)

            input: UserInput = UserInput()

            for strategy_input_dict in data:
                strategy_input_obj: StrategyInput = StrategyInput(
                    strategy_input_dict['strategy_type'],
                    strategy_input_dict['should_run'],
                    strategy_input_dict['trade_type'],
                    strategy_input_dict['market'],
                    strategy_input_dict['lot_qty'],
                )

                input._append_strategy_input(strategy_input_obj)

            return input
