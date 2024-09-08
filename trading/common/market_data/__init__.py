from kiteconnect import KiteConnect
from trading.broker.kite import config as kite_config
from trading.common.market_data.market_data_manager import MarketDataManager


def new_kite_connect_client() -> KiteConnect:
    kc: KiteConnect = KiteConnect(
        api_key=kite_config.API_KEY,
    )

    print("Please login with here and fetch the 'request_token' from redirected "
          "url after successful login : ", kc.login_url())

    request_token: str = input("enter 'request_token': ")

    session_data: dict = kc.generate_session(
        request_token=request_token,
        api_secret=kite_config.API_SECRETE,
    )

    kite_config.ACCESS_TOKEN = session_data['access_token']
    kc.set_access_token(kite_config.ACCESS_TOKEN)

    print('\nkite connect client creation successful !!! ')

    return kc


def initialise_market_data_fetcher_client():
    kc: KiteConnect = new_kite_connect_client()
    MarketDataManager.bootstrap(kc)
