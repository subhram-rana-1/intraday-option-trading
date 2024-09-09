from trading.common.enums import Market
from trading.common.exceptions import InvalidMarket


def improvisation(func):
    def wrapper(*args, **kwargs):
        pass

    return wrapper


def get_lot_size(market: Market) -> int:
    if market == Market.NIFTY:
        return 25
    elif market == Market.BANKNIFTY:
        return 15

    raise InvalidMarket(market.value)


def get_quantity_from_lot_quantity(market: Market, lot_qty: int) -> int:
    return get_lot_size(market) * lot_qty
