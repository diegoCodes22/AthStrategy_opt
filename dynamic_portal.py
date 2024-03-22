from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import Order
from ibapi.contract import Contract
from typing import List


class DynamicPortal(EClient, EWrapper):
    def __init__(self, orders: List[Order], contract: Contract):
        EClient.__init__(self, self)
        for order in orders:
            self.placeOrder(order.orderId, contract, order)

    def openOrderEnd(self):
        self.disconnect()
