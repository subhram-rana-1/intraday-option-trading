from kiteconnect import KiteTicker

from trading.broker.kite.config import ACCESS_TOKEN, API_KEY


def new_kite_websocket_client() -> KiteTicker:
    if ACCESS_TOKEN is None:
        err_msg = ('access_token is not initialised. Please connect to kite connect first with'
                   ' "get_kite_connect_client()" function, and then try to create websocket client')

        raise Exception(err_msg)

    kws: KiteTicker = KiteTicker(
        api_key=API_KEY,
        access_token=ACCESS_TOKEN,
    )

    print('\nkite websocket client creation successful !!! ')

    return kws
