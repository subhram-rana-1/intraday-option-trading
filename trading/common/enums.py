from enum import Enum


def choices_from_enum(cls: Enum):
    return [(item.name, item.value) for item in cls]


class DjangoEnum(Enum):
    @classmethod
    def choices(cls):
        return choices_from_enum(cls)


class TradeType(DjangoEnum):
    PAPER = 'PAPER'
    LIVE = 'LIVE'


class Market(DjangoEnum):
    NIFTY = 'NIFTY'
    BANKNIFTY = 'BANKNIFTY'


class StrategyType(DjangoEnum):
    LONG_MOMENTUM_CALL = 'LONG_MOMENTUM_CALL'
    LONG_MOMENTUM_PUT = 'LONG_MOMENTUM_PUT'
    SHORT_STRANGLE = 'SHORT_STRANGLE'


class Broker(DjangoEnum):
    ZERODHA = 'ZERODHA'
    UPSTOX = 'UPSTOX'
    BROKER_SIMULATOR = 'BROKER_SIMULATOR'


class TradeState(DjangoEnum):
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class TxnType(DjangoEnum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderPriceType(DjangoEnum):
    BUY = 'MARKET'
    SELL = 'LIMIT'


class OrderStatus(DjangoEnum):
    CREATED = 'CREATED'
    BROKER_PENDING = 'BROKER_PENDING'
    CONFIRMED = 'CONFIRMED'
