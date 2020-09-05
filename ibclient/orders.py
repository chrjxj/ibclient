# coding=utf-8

'''
Provide Application layer Order definitions.
The implementation refers to https://interactivebrokers.github.io/tws-api/basic_orders.html


Created on  04/2020
@author: Jin Xu
@contact: jin_xu1@qq.com
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from ib.ext.Order import Order


class OrderExecution():
    """ Order Execution Details """
    Filled = "Filled"
    PreSubmitted = "PreSubmitted"
    NotFound = "NotFound"

    def __init__(self, orderId, status, filled, remaining,
                 avgFillPrice, permId, parentId,
                 lastFillPrice, clientId, whyHeld):
        self.client_id = clientId
        self.order_id = orderId
        self.parent_id = parentId
        self.status = status
        self.filled = bool(filled)
        self.permId = int(permId)
        self.remaining = int(remaining)
        self.avgFillPrice = float(avgFillPrice)
        self.lastFillPrice = float(lastFillPrice)
        self.whyHeld = whyHeld

    def update(self, orderId, status, filled, remaining,
                 avgFillPrice, permId, parentId,
                 lastFillPrice, clientId, whyHeld):

        if clientId == self.client_id and orderId == self.order_id:

            self.status = status
            self.filled = bool(filled)
            self.permId = int(permId)
            self.remaining = int(remaining)
            self.avgFillPrice = float(avgFillPrice)
            self.lastFillPrice = float(lastFillPrice)
            self.whyHeld = whyHeld
        else:
            raise ValueError("Found clientId and/or orderId mismatch.")


class OrderType():
    """ Order Execution Status """
    Market = "MKT"
    Limit = "LMT"
    Stop = "STP"
    StopLimit = "STP LMT"


class OrderBase(Order):
    ''' Define IB order type.
    '''

    def __init__(self, order_type, limit_price=None, stop_price=None):
        """

        :param order_type:
        :param limit_price:
        :param stop_price:
        """
        super(OrderBase, self).__init__()

        self.order_type = order_type

        if order_type == OrderType.Market:
            pass
        elif order_type == OrderType.Limit:
            if limit_price is not None:
                self.m_lmtPrice = limit_price
            else:
                raise ValueError
        elif order_type == OrderType.Limit:
            if stop_price is not None:
                self.m_auxPrice = stop_price
            else:
                raise ValueError
        else:
            raise NotImplementedError

        self.is_combo_order = False
        self.non_guaranteed = False
        self.__order_id = -1
        self.m_overridePercentageConstraints = True  # override TWS order size constraints

    @property
    def client_id(self):
        return self.m_client_id

    @client_id.setter
    def client_id(self, client_id: int):
        assert client_id > 0, "Order ID in TWS must be a positive int."
        self.m_client_id = client_id

    @property
    def ID(self):
        return self.m_orderId

    @ID.setter
    def ID(self, order_id: int):
        """
        Set order id. User needs to request a valid order ID from TWS host
        using self.connection.reqIds(-1), and then set order ID.
        see details: https://interactivebrokers.github.io/tws-api/order_submission.html

        :param order_id: int

        """
        assert order_id > 0, "Order ID in TWS must be a positive int."
        self.m_orderId = order_id

    @property
    def action(self):
        return self.m_action

    @action.setter
    def action(self, action: str):
        self.m_action = action

    @property
    def amount(self):
        return self.m_totalQuantity

    @amount.setter
    def amount(self, amount: int):
        self.m_totalQuantity = abs(amount)

    @property
    def order_type(self):
        return self.m_orderType

    @order_type.setter
    def order_type(self, order_type):
        self.m_orderType = order_type

    @property
    def limit_price(self):
        return self.m_lmtPrice

    @property
    def stop_price(self):
        return self.m_auxPrice

    def __str__(self):
        return '{} order: limit price: {}, stop price: {}, ' \
               'Combo order: {}, Guaranteed: {}'.format(self.order_type, self.limit_price,
                                                        self.stop_price, self.is_combo_order, not self.non_guaranteed)

    def __repr__(self):
        pass


class MarketOrder(OrderBase):
    ''' Market Order '''

    def __init__(self):
        super(MarketOrder, self).__init__('MKT')


class LimitOrder(OrderBase):
    ''' Define Limit order type.
    '''

    def __init__(self, limit_price):
        super(LimitOrder, self).__init__('LMT', limit_price=limit_price)


class StopOrder(OrderBase):
    ''' Define Stop order type.
    '''

    def __init__(self, stop_price):
        super(StopOrder, self).__init__('STP', stop_price=stop_price)
        raise NotImplementedError


class StopLimitOrder(OrderBase):
    ''' Define Stop Limit order type.
    '''

    def __init__(self, limit_price, stop_price):
        super(StopLimitOrder, self).__init__('STP LMT',
                                             limit_price=limit_price,
                                             stop_price=stop_price)
        raise NotImplementedError


class ComboMarketOrder(OrderBase):
    ''' Define IB Combo Market Order type.
    '''

    def __init__(self):
        super(ComboMarketOrder, self).__init__('MKT')
        self.is_combo_order = True
        self.non_guaranteed = True
        raise NotImplementedError


class ComboLimitOrder(OrderBase):
    ''' Define IB Combo Limit Order type.
    '''

    def __init__(self, limit_price):
        super(ComboLimitOrder, self).__init__('LMT', limit_price=limit_price)
        self.is_combo_order = True
        self.non_guaranteed = True
        raise NotImplementedError
