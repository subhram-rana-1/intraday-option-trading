import threading

from django.core.management.base import BaseCommand

from trading.common.entities.user_input import UserInput, StrategyInput
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
        user_input: UserInput = UserInput.from_json_file()

        for strategy_input in user_input.strategy_inputs:
            async_start_strategy(strategy_input)
