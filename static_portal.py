from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import TickerId, BarData
from ibapi.tag_value import TagValue
from ibapi.scanner import ScannerSubscription
from ibapi.contract import ContractDetails
from globals import CLIENT_ID, top_stocks, YESTERDAY
from utils import ohlcv_dataframe


class StaticPortal(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextOrderId = 0
        self.hist_data = []

    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(errorCode, errorString)

    def build_scanner(self):
        sub = ScannerSubscription()
        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "HIGH_VS_52W_HL"
        sub.numberOfRows = 4
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
        top_stocks[rank] = {"contract": contractDetails.contract}

    def scannerDataEnd(self, reqId: int):
        self.cancelScannerSubscription(CLIENT_ID)

        for rank in top_stocks:
            pass

    def algorithm(self, rank):
        self.reqHistoricalData(rank, top_stocks[rank]["contract"], YESTERDAY, "60 D", "1 day", 'TRADES', 1, 1, False, [])

    def historicalData(self, reqId: int, bar: BarData):
        self.hist_data.append(bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        df = ohlcv_dataframe(self.hist_data)

