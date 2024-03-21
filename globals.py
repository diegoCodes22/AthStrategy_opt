from datetime import datetime
from pytz import timezone


MKT_OPEN = "09:30:00"
HOST = "127.0.0.1"
PORT = 7497
CLIENT_ID = 1001
YESTERDAY = datetime.now(timezone("US/Eastern")).replace(hour=9, minute=00, second=0).strftime("%Y%m%d %H:%M:%S")
top_stocks = {}