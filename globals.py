from datetime import datetime
from pytz import timezone

# {rank: {conId: conId, htf_atr: htf_atr, quantity: quantity, last: last}}
top_stocks = {}
strat_buys = {}

MKT_OPEN = "09:30:00"
MKT_CLOSE = "16:30:00"
YESTERDAY = datetime.now(timezone("US/Eastern")).replace(hour=9, minute=00, second=0).strftime("%Y%m%d %H:%M:%S")

# Project configurations
ATR_LEN = 14
TRADE_SIZE = 500
ATR_PRC = 1.5
CANCEL_AFTER = 30
MAX_TRADES = 4
MAX_ROWS = 8
RISK_REWARD = 2.5

# TWS connection settings
HOST = "127.0.0.1"
PORT = 7497
CLIENT_ID = 1001
