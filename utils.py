from ibapi.common import BarData
from pandas import DataFrame

from typing import List
from time import sleep
from datetime import datetime
from pytz import timezone
from globals import MKT_OPEN


def sleep_till_open() -> None:
    ct = datetime.now(timezone("US/Eastern")).strftime("%H:%M:%S")
    ct = datetime.strptime(ct, "%H:%M:%S")
    mkt = datetime.strptime(MKT_OPEN, "%H:%M:%S")
    seconds_till_open = (mkt - ct).total_seconds()
    sleep(seconds_till_open)


def ohlcv_dataframe(bars: List[BarData]) -> DataFrame:
    data = []
    for bar in bars:
        data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])
    return DataFrame(data, columns=["date", "open", "high", "low", "close", "volume"])