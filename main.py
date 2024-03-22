from threading import Thread
from static_portal import StaticPortal
from dynamic_portal import DynamicPortal
from utils import sleep_till_open
from globals import strat_buys, HOST, PORT, CLIENT_ID


def static_connect() -> None:
    sp = StaticPortal()
    sp.connect(HOST, PORT, CLIENT_ID)
    sp.run()


def dynamic_connect() -> None:
    for rank in strat_buys:
        dp = DynamicPortal(strat_buys[rank]["bracket"], strat_buys[rank]["contract"])
        dp.connect(HOST, PORT, CLIENT_ID)
        Thread(target=dp.run, args=()).start()


def main() -> None:
    sleep_till_open()
    static_connect()
    dynamic_connect()


if __name__ == "__main__":
    main()
