from ibapi.order import Order
from ibapi.order_condition import OrderCondition, Create
from datetime import datetime, timedelta
from pytz import timezone
from globals import *


# Maybe add MOC orders to transmit if mkt close is approaching and position is still open


def bracket(rank: int) -> list:
    contract = strat_buys[rank]["contract"]
    last = strat_buys[rank]["last"]
    quantity = strat_buys[rank]["quantity"]
    htf_atr = strat_buys[rank]["htf_atr"]
    oid = strat_buys[rank]["order_id"]

    diff = round(htf_atr * TARGET_MULTIPLIER, 2)
    tp_target = round(last + diff, 2)

    parent = Order()
    parent.orderId = oid
    parent.totalQuantity = quantity
    parent.action = "BUY"
    parent.tif = "GTD"
    parent.goodTillDate = parent.goodTillDate = (datetime.now(timezone("US/Eastern")) + timedelta(minutes=CANCEL_AFTER)).strftime("%Y%m%d %H:%M:%S") + " US/Eastern"
    parent.transmit = True
    parent.orderType = "TRAIL LIMIT"
    parent.trailStopPrice = last * 1.003
    parent.trailingPercent = 0.2
    parent.lmtPriceOffset = round(parent.trailStopPrice * OFFSET_PRC, 2)

    # Take profit
    take_profit = Order()
    take_profit.orderId = oid + 1
    take_profit.totalQuantity = parent.totalQuantity
    take_profit.action = "SELL"
    take_profit.tif = "DAY"
    take_profit.transmit = True
    take_profit.orderType = "TRAIL LIMIT"
    take_profit.trailStopPrice = round(tp_target - diff, 2)
    take_profit.trailingPercent = 1
    take_profit.lmtPriceOffset = round(take_profit.trailStopPrice * OFFSET_PRC, 2)

    # Stop loss
    stop_loss = Order()
    stop_loss.orderId = oid + 2
    stop_loss.totalQuantity = parent.totalQuantity
    stop_loss.action = "SELL"
    stop_loss.tif = "DAY"
    stop_loss.transmit = True
    stop_loss.orderType = "STP LMT"
    stop_loss.auxPrice = round(last - (htf_atr / RISK_REWARD), 2)
    stop_loss.lmtPrice = round(stop_loss.auxPrice - (stop_loss.auxPrice * OFFSET_PRC), 2)

    # Market on Close
    moc = Order()
    moc.orderId = oid + 3
    moc.totalQuantity = parent.totalQuantity
    moc.action = "SELL"
    moc.orderType = "MOC"

    # Order conditions
    tp_condition = Create(OrderCondition.Price)
    tp_condition.conId = contract.conId
    tp_condition.exchange = contract.exchange
    tp_condition.isMore = True
    tp_condition.triggerMethod = 2
    tp_condition.price = tp_target
    # AND trade occurs for contract
    take_profit.conditions.append(tp_condition)

    # for stop loss and moc trade occurs on contract

    # OCA grouping
    take_profit.ocaGroup = contract.symbol
    take_profit.ocaType = 1

    stop_loss.ocaGroup = contract.symbol
    stop_loss.ocaType = 1

    moc.ocaGroup = contract.symbol
    moc.ocaType = 1

    return [parent, take_profit, stop_loss]
