from datetime import datetime
from pytz import timezone

# {rank: {conId: conId, htf_atr: htf_atr, quantity: quantity, last: last, oid: oid}}
top_stocks = {}
strat_buys = {}

# Constants
MKT_OPEN = "09:30:00"
MKT_CLOSE = "16:30:00"
YESTERDAY = datetime.now(timezone("US/Eastern")).replace(hour=9, minute=00, second=0).strftime("%Y%m%d %H:%M:%S")
ORDER_ID_RANGE = 5

# Project configurations
ATR_LEN = 14
TRADE_SIZE = 500
ATR_PRC = 1.5
CANCEL_AFTER = 30
MAX_TRADES = 4
MAX_ROWS = 8
RISK_REWARD = 2.5
TARGET_MULTIPLIER = 0.05
OFFSET_PRC = 0.0005

# TWS connection settings
HOST = "127.0.0.1"
PORT = 7497
CLIENT_ID = 1001
