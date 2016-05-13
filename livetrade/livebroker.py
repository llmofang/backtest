import queue
from pyalgotrade import broker
from pyalgotrade.bitstamp import common

class LiveBroker(broker.Broker):
    def __init__(self):
        broker.Broker.__init__(self)
        self.__shares={}
        self.__cash=0
        self.__activeOrders={}

    def getInstrumentTraits(self, instrument):
        return common.BTCTraits()

    def createLimitOrder(self,action,instrument,limitprice,quantity):
        if action == broker.Order.Action.BUY_TO_COVER:
            action = broker.Order.Action.BUY
        elif action == broker.Order.Action.SELL_SHORT:
            action = broker.Order.Action.SELL
        if action not in [broker.Order.Action.BUY, broker.Order.Action.SELL]:
            raise Exception("Only BUY/SELL orders are supported")
        instrumentTraits = self.getInstrumentTraits(instrument)
        return broker.LimitOrder(action,instrument,limitprice,quantity,instrumentTraits)

    def submitOrder(self,order):
        #TODO 订单提交到
        pass

    def getCash(self, includeShort=True):
        return self.__cash

    def getShares(self, instrument):
        return self.__shares.get(instrument,0)

    def getPositions(self):
        return self.__shares

    def getActiveOrders(self, instrument=None):
         return list(self.__activeOrders.values())

    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        pass


    def createStopOrder(self, action, instrument, stopPrice, quantity):
        pass

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        pass

    def cancelOrder(self, order):
        activeOrder = self.__activeOrders.get(order.getId())
        if activeOrder is None:
            raise Exception("The order is not active anymore")
        if activeOrder.isFilled():
            raise Exception("Can't cancel order that has already been filled")
        #TODO 取消订单

        #TODO??订单取消不一定成功 在回调函数中更改状态？？
        order.switchState(broker.Order.State.CANCELED)
        self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.CANCELED, "User requested cancellation"))


    def dispatch(self):
         # Switch orders from SUBMITTED to ACCEPTED.
        ordersToProcess = list(self.__activeOrders.values())
        for order in ordersToProcess:
            if order.isSubmitted():
                order.switchState(broker.Order.State.ACCEPTED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.ACCEPTED, None))

        # Dispatch events from the trade monitor.
        try:
            eventType, eventData = self.__tradeMonitor.getQueue().get(True, LiveBroker.QUEUE_TIMEOUT)

            if eventType == TradeMonitor.ON_USER_TRADE:
                self._onUserTrades(eventData)
            else:
                common.logger.error("Invalid event received to dispatch: %s - %s" % (eventType, eventData))
        except queue.Empty:
            pass