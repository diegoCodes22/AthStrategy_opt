from ibapi.order import Order
from datetime import datetime, timedelta
from pytz import timezone
from globals import top_stocks, CANCEL_AFTER, RISK_REWARD


# Maybe add MOC orders to transmit if mkt close is approaching and position is still open


def bracket(rank: int) -> list:
    last = top_stocks[rank]["last"]
    quantity = top_stocks[rank]["quantity"]
    htf_atr = top_stocks[rank]["htf_atr"]

    parent = Order()
    # parent.orderId
    parent.totalQuantity = quantity
    parent.action = "BUY"
    parent.tif = "GTD"
    parent.goodTillDate = parent.goodTillDate = (datetime.now(timezone("US/Eastern")) + timedelta(minutes=CANCEL_AFTER)).strftime("%Y%m%d %H:%M:%S") + " US/Eastern"
    parent.transmit = True
    parent.orderType = "TRAIL LIMIT"
    parent.trailStopPrice = last * 1.003
    parent.trailingPercent = 0.2
    parent.lmtPriceOffset = round(parent.trailStopPrice * 0.0005, 2)

    take_profit = Order()
    # take_profit.orderId
    # take_profit.parentId
    take_profit.totalQuantity = parent.totalQuantity
    take_profit.action = "SELL"
    take_profit.tif = "DAY"
    take_profit.transmit = True
    take_profit.orderType = "TRAIL LIMIT"
    take_profit.trailStopPrice = round(last + htf_atr, 2)
    take_profit.trailingPercent = 1
    take_profit.lmtPriceOffset = round(take_profit.trailStopPrice * 0.0005, 2)

    stop_loss = Order()
    # stop_loss.orderId
    # stop_loss.parentId
    stop_loss.totalQuantity = parent.totalQuantity
    stop_loss.action = "SELL"
    stop_loss.tif = "DAY"
    stop_loss.transmit = True
    stop_loss.orderType = "STP LMT"
    stop_loss.auxPrice = round(last - (htf_atr / RISK_REWARD), 2)
    stop_loss.lmtPrice = round(stop_loss.auxPrice - (stop_loss.auxPrice * 0.0005), 2)

    return [parent, take_profit, stop_loss]
