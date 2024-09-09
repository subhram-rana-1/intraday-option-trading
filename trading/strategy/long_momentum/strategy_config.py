from datetime import time
from typing import List
from trading.common.entities.time_range import TimeRange


class LongMomentumStrategyConfig:
    max_square_off_time: time = time(15, 25, 0)
    allowed_time_ranges_for_entry: List[TimeRange] = [
        TimeRange(
            start=time(9, 16, 0),
            end=time(12, 0, 0),
        ),
        TimeRange(
            start=time(14, 30, 0),
            end=time(15, 15, 0),
        )
    ]
    root_sl_deviation_pt = 6
    min_profit_pt = 10
    max_allowed_price_fluctuation_pt = 10

    @property
    def min_entry_time(self) -> time:
        return self.allowed_time_ranges_for_entry[0].start

    @property
    def max_entry_time(self) -> time:
        return self.allowed_time_ranges_for_entry[-1].end
