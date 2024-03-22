from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import TickerId, BarData, TickAttrib
from ibapi.tag_value import TagValue
from ibapi.scanner import ScannerSubscription
from ibapi.contract import ContractDetails
from ibapi.ticktype import TickType
from pandas_ta.volatility import atr
from time import sleep
from globals import *
from utils import ohlcv_dataframe
from bracket import bracket


class StaticPortal(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextOrderId = 0
        self.sde = 0
        self.hist_data = []

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        self.reqMarketDataType(2)
        self.build_scanner()

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(errorCode, errorString)

    def build_scanner(self):
        sub = ScannerSubscription()
        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "HIGH_VS_52W_HL"
        sub.numberOfRows = MAX_ROWS
        sub.abovePrice = 10
        sub.belowPrice = 500
        scan_options = []
        filter_options = [
            TagValue("avgVolumeAbove", "100000"),
            TagValue("rcgShortTermEventScoreAbove", "0.5"),
            TagValue("socialSentimentScoreAbove", "0.5"),
            TagValue("tweetVolumeScoreAbove", "0.5"),
            TagValue("haltedIs", "false"),
            TagValue("shortSaleRestrictionIs", "false")
        ]
        self.reqScannerSubscription(CLIENT_ID, sub, scan_options, filter_options)

    def scannerData(self, reqId: int, rank: int, contractDetails: ContractDetails,
                    distance: str, benchmark: str, projection: str, legsStr: str):
        top_stocks[rank+1] = {"contract": contractDetails.contract}

    def scannerDataEnd(self, reqId: int):
        self.cancelScannerSubscription(CLIENT_ID)
        self.sde = 1
        # self.algorithm()

    def reqHist(self, rank):
        self.hist_data.clear()
        self.reqHistoricalData(rank, top_stocks[rank]["contract"], YESTERDAY, "60 D", "1 day", 'TRADES', 1, 1, False, [])

    # def algorithm(self):
    #     for rank in top_stocks:
    #         self.reqHist(rank)
    #         sleep(5)
    #     c = 1
    #     for k, v in list(top_stocks.items())[:MAX_TRADES]:
    #         v["order_id"] = CLIENT_ID + (ORDER_ID_RANGE * c)
    #         v["bracket"] = bracket(k)
    #         strat_buys[k] = v
    #         c += 1
    #     print(top_stocks)

    def historicalData(self, reqId: int, bar: BarData):
        self.hist_data.append(bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        df = ohlcv_dataframe(self.hist_data)
        top_stocks[reqId]["htf_atr"] = round(atr(df["high"], df["low"], df["close"], ATR_LEN).iloc[-1], 2)
        # self.reqMktData(reqId, top_stocks[reqId]["contract"], "", False, False, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        if tickType == 4:
            try:
                top_stocks[reqId]["last"] = price
                top_stocks[reqId]["quantity"] = round(TRADE_SIZE / price)
                assert round((top_stocks[reqId]["htf_atr"] / price) * 100, 3) > ATR_PRC
            except AssertionError:
                del top_stocks[reqId]
            except KeyError:
                pass
            self.cancelMktData(reqId)
