from threading import Thread
import sys
from static_portal import StaticPortal
from dynamic_portal import DynamicPortal
from utils import sleep_till_open
from globals import strat_buys, top_stocks, HOST, PORT, CLIENT_ID, MAX_TRADES, ORDER_ID_RANGE
from time import sleep


def algo(sp: StaticPortal):
    while sp.sde == 0:
        continue
    for rank in range(1, len(top_stocks) + 1):
        sp.reqHist(rank)
        while "htf_atr" not in top_stocks[rank]:
            continue
        sp.reqMktData(rank, top_stocks[rank]["contract"], "", False, False, [])
        try:
            while "quantity" not in top_stocks[rank]:
                continue
        except KeyError:
            pass
    for k, v in list(top_stocks.items())[:MAX_TRADES]:
        strat_buys[k] = v
    sp.disconnect()


def static_connect() -> None:
    sp = StaticPortal()
    sp.connect(HOST, PORT, CLIENT_ID)
    Thread(target=sp.run, args=(), daemon=True).start()
    sleep(0.5)
    algo(sp)


def dynamic_connect() -> None:
    for i, rank in enumerate(strat_buys, 1):
        dp = DynamicPortal(rank, strat_buys[rank]["contract"])
        dp.connect(HOST, PORT, CLIENT_ID + i)
        Thread(target=dp.run, args=()).start()


def main() -> None:
    sleep_till_open()
    static_connect()
    dynamic_connect()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = 7496
    else:
        PORT = 7497
    main()
