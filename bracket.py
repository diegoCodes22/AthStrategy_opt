from datetime import timedelta
from ibapi.order import Order
from globals import *


def bracket(rank: int) -> list:
    last = strat_buys[rank]["last"]
    quantity = strat_buys[rank]["quantity"]
    htf_atr = strat_buys[rank]["htf_atr"]
    oid = strat_buys[rank]["order_id"]

    diff = round(htf_atr * TARGET_MULTIPLIER, 2)
    tp_target = round(last + diff, 2)

    # Entry
    parent = Order()
    parent.orderId = oid
    parent.totalQuantity = quantity
    parent.action = "BUY"
    parent.tif = "GTD"
    parent.goodTillDate = parent.goodTillDate = (datetime.now(timezone("US/Eastern")) + timedelta(minutes=CANCEL_AFTER)).strftime("%Y%m%d %H:%M:%S") + " US/Eastern"
    parent.transmit = False
    parent.orderType = "TRAIL LIMIT"
    parent.trailStopPrice = last * 1.003
    parent.trailingPercent = 0.2
    parent.lmtPriceOffset = round(parent.trailStopPrice * OFFSET_PRC, 2)

    # Market on Close
    moc = Order()
    moc.orderId = oid + 1
    moc.parentId = parent.orderId
    moc.totalQuantity = parent.totalQuantity
    moc.action = "SELL"
    moc.orderType = "MOC"
    moc.transmit = False

    # Adjustable exit
    exit_order = Order()
    exit_order.orderId = oid + 2
    exit_order.parentId = parent.orderId
    exit_order.totalQuantity = parent.totalQuantity
    exit_order.action = "SELL"
    exit_order.tif = "DAY"
    exit_order.transmit = True
    exit_order.orderType = "STP LMT"
    exit_order.auxPrice = round(last - (htf_atr / RISK_REWARD), 2)
    exit_order.lmtPrice = round(exit_order.auxPrice - (exit_order.auxPrice * OFFSET_PRC), 2)

    exit_order.triggerPrice = tp_target
    exit_order.adjustedOrderType = "TRAIL LIMIT"
    exit_order.adjustedStopPrice = round(tp_target - diff, 2)
    exit_order.adjustableTrailingUnit = 1
    exit_order.adjustedTrailingAmount = 1
    exit_order.adjustedStopLimitPrice = round(exit_order.adjustedStopPrice - (exit_order.adjustedStopPrice * OFFSET_PRC), 2)

    print(f"{parent}\n{exit_order}\nTrail trigger @ {tp_target}")
    return [parent, moc, exit_order]
