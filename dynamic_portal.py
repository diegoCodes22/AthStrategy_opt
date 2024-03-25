from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import OrderId, Decimal
from ibapi.contract import Contract
from bracket import bracket


class DynamicPortal(EClient, EWrapper):
    def __init__(self, rank: int, contract: Contract):
        EClient.__init__(self, self)
        self.rank = rank
        self.contract = contract
        self.parentId = 0

    def nextValidId(self, orderId: int):
        self.parentId = orderId
        orders = bracket(self.rank, self.parentId)
        for order in orders:
            self.placeOrder(order.orderId, self.contract, order)

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal,
                    remaining: Decimal, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        if orderId == self.parentId and status == "PreSubmitted":
            self.disconnect()
