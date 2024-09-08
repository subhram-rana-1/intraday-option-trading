from enum import Enum


class TradeType(Enum):
    PAPER = 'PAPER'
    LIVE = 'LIVE'


class Market(Enum):
    NIFTY = 'NIFTY'
    BANKNIFTY = 'BANKNIFTY'


class StrategyType(Enum):
    LONG_MOMENTUM_CALL = 'LONG_MOMENTUM_CALL'
    LONG_MOMENTUM_PUT = 'LONG_MOMENTUM_PUT'
    SHORT_STRANGLE = 'SHORT_STRANGLE'
