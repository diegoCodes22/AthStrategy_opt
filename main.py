from threading import Thread
from static_portal import StaticPortal
from dynamic_portal import DynamicPortal
from utils import sleep_till_open
from globals import strat_buys, top_stocks, HOST, PORT, CLIENT_ID, MAX_TRADES, ORDER_ID_RANGE
from bracket import bracket
from time import sleep


def mp_strat() -> None:
    c = 0
    for k, v in list(top_stocks.items())[:MAX_TRADES]:
        v["order_id"] = CLIENT_ID + (ORDER_ID_RANGE * c)
        strat_buys[k] = v
        strat_buys[k]["bracket"] = bracket(k)
        c += 1


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
    mp_strat()


def static_connect() -> StaticPortal:
    sp = StaticPortal()
    sp.connect(HOST, PORT, CLIENT_ID)
    Thread(target=sp.run, args=()).start()
    sleep(0.5)
    return sp


def dynamic_connect() -> None:
    for i, rank in enumerate(strat_buys, 1):
        dp = DynamicPortal(strat_buys[rank]["bracket"], strat_buys[rank]["contract"])
        dp.connect(HOST, PORT, CLIENT_ID + i)
        Thread(target=dp.run, args=()).start()


def main() -> None:
    sleep_till_open()
    sc = static_connect()
    algo(sc)
    dynamic_connect()


if __name__ == "__main__":
    main()
