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


class Broker(Enum):
    ZERODHA = 'ZERODHA'
    UPSTOX = 'UPSTOX'
    BROKER_SIMULATOR = 'BROKER_SIMULATOR'


class TradeState(Enum):
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class TxnType(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderPriceType(Enum):
    BUY = 'MARKET'
    SELL = 'LIMIT'


class OrderStatus(Enum):
    CREATED = 'CREATED'
    BROKER_PENDING = 'BROKER_PENDING'
    CONFIRMED = 'CONFIRMED'
