from ibapi.client import EClient
from ibapi.wrapper import EWrapper


# I would like to transmit first the entry order, and only transmit the stop loss if the entry order is filled
# Transmit trailing take profit after it reaches target price
#   (lower target price)
# Cancel stop loss after transmitting take profit

class DynamicPortal(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

