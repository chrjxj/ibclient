# coding=utf-8

'''
Define Order types
Created on  04/2020
@author: Jin Xu
@contact: jin_xu1@qq.com
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


class OrderStyle(object):
    ''' Define IB order type.
    '''

    def __init__(self, order_type='MKT', limit_price=None, stop_price=None):
        self.order_type = order_type
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.is_combo_order = False
        self.non_guaranteed = False

    def __str__(self):
        return '{} order: limit price: {}, stop price: {}, ' \
               'Combo order: {}, Guaranteed: {}'.format(self.order_type, self.limit_price,
                                                        self.stop_price, self.is_combo_order, not self.non_guaranteed)

    def __repr__(self):
        pass


class MarketOrder(OrderStyle):
    ''' Define Market Order type.
    '''

    def __init__(self):
        super(MarketOrder, self).__init__(order_type='MKT')


class LimitOrder(OrderStyle):
    ''' Define Limit order type.
    '''

    def __init__(self, limit_price):
        super(LimitOrder, self).__init__(order_type='LMT', limit_price=limit_price)


class StopOrder(OrderStyle):
    ''' Define Stop order type.
    '''

    def __init__(self, stop_price):
        super(StopOrder, self).__init__(order_type='STP', stop_price=stop_price)


class StopLimitOrder(OrderStyle):
    ''' Define Stop Limit order type.
    '''

    def __init__(self, limit_price, stop_price):
        super(StopLimitOrder, self).__init__(order_type='STP LMT', limit_price=limit_price, stop_price=stop_price)


class ComboMarketOrder(OrderStyle):
    ''' Define IB Combo Market Order type.
    '''

    def __init__(self):
        super(ComboMarketOrder, self).__init__(order_type='MKT')
        self.is_combo_order = True
        self.non_guaranteed = True


class ComboLimitOrder(OrderStyle):
    ''' Define IB Combo Limit Order type.
    '''

    def __init__(self, limit_price):
        super(ComboLimitOrder, self).__init__(order_type='LMT', limit_price=limit_price)
        self.is_combo_order = True
        self.non_guaranteed = True
