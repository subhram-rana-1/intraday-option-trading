from datetime import time

import pytz

user_input_json_file_relative_path = 'trading/user_input.json'
market_start_time = time(9, 15, 0)
market_end_time = time(15, 30, 0)

trading_symbol_nifty_50 = 'NIFTY 50'
trading_symbol_banknifty = 'NIFTY BANK'

IST_timezone = pytz.timezone('Asia/Kolkata')
