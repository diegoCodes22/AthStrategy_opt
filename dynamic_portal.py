from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import Order
from ibapi.common import OrderId, Decimal
from ibapi.contract import Contract
from typing import List


class DynamicPortal(EClient, EWrapper):
    def __init__(self, orders: List[Order], contract: Contract):
        EClient.__init__(self, self)
        self.orders = orders
        self.contract = contract

    def nextValidId(self, orderId: int):
        print(orderId)
        for order in self.orders:
            self.placeOrder(order.orderId, self.contract, order)

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal,
                    remaining: Decimal, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        if remaining == Decimal(0):
            self.disconnect()
