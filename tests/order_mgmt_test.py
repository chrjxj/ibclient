# -*- coding:utf-8 -*-
'''
Created on 11/08/2016
@author: Jin Xu
'''
import sys
from os import path
import unittest
import datetime
import time
from pprint import pprint
import random

from ibclient import (IBClient,
                      MarketOrder, LimitOrder,
                      new_stock_contract, new_futures_contract)

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))
from tests.config import load_config


class Test(unittest.TestCase):

    def setUp(self):
        self.config = load_config('test-acc.yaml')
        pprint(self.config)
        _stock_config = self.config['stock']
        self.stock = new_stock_contract(_stock_config['symbol'],
                                        exchange = _stock_config['exchange'],
                                        currency=_stock_config['currency'])

        self.future = new_futures_contract(self.config['future']['symbol'],
                                           self.config['future']['exchange'],
                                           False,
                                           expiry=str(self.config['future']['expiry']),
                                           tradingClass=self.config['future']['tradingClass'])
        self.end = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')

        self.con = IBClient(port=self.config['port'],
                            client_id=random.randint(1, 10000))
        self.con.connect()

    def tearDown(self):
        self.con.disconnect()

    def test01_get_open_orders(self):
        print('%s test_get_open_orders %s' % ('-' * 30, '-' * 30))

        # order MSFT at $10 - this will create a pending order
        id1 = self.con.order_amount(self.stock, 100, style=LimitOrder(10.))
        time.sleep(0.2)
        id2 = self.con.order_amount(self.future, -1, style=LimitOrder(10.))
        time.sleep(1)
        id3 = self.con.order_amount(self.future, -1, style=MarketOrder())
        time.sleep(1)

        self.con.get_open_orders()
        time.sleep(5)
        for key in self.con.order_dict:
            print('%s' % '-' * 60)
            if 'order' in self.con.order_dict[key]:
                order = self.con.order_dict[key]['order']
                print('m_orderId       = %d' % order.m_orderId)
                print('m_clientId      = %d' % order.m_clientId)
                print('m_permId        = %d' % order.m_permId)
                print('m_action        = %s' % order.m_action)
                print('m_totalQuantity = %d' % order.m_totalQuantity)
                print('m_orderType     = %s' % order.m_orderType)
            if 'contract' in self.con.order_dict[key]:
                contract = self.con.order_dict[key]['contract']
                print('contract        = %d' % contract.m_conId)

            print('status', ' ', self.con.order_dict[key]['status'])
            print('filled', ' ', self.con.order_dict[key]['filled'])
            print('permId', ' ', self.con.order_dict[key]['permId'])
            print('remaining', ' ', self.con.order_dict[key]['remaining'])
            print('avgFillPrice', ' ', self.con.order_dict[key]['avgFillPrice'])
            print('lastFillPrice', ' ', self.con.order_dict[key]['lastFillPrice'])
            print('whyHeld', ' ', self.con.order_dict[key]['whyHeld'])

        time.sleep(0.5)

    def test02_cancel_orders(self):
        print('%s test_cancel_orders %s' % ('-' * 30, '-' * 30))

        # order MSFT at $10 - this will create a pending order
        id1 = self.con.order_amount(self.stock, 100, style=LimitOrder(10.))
        time.sleep(0.5)
        id2 = self.con.order_amount(self.future, -1, style=LimitOrder(10.))
        time.sleep(0.5)
        id3 = self.con.order_amount(self.stock, -100, style=LimitOrder(80.))
        time.sleep(0.5)

        self.con.get_open_orders()
        time.sleep(5)
        for key in self.con.order_dict:
            print('%s' % '-' * 60)
            if 'order' in self.con.order_dict[key]:
                order = self.con.order_dict[key]['order']
                print('m_orderId       = %d' % order.m_orderId)
                print('m_clientId      = %d' % order.m_clientId)
                print('m_permId        = %d' % order.m_permId)
                print('m_action        = %s' % order.m_action)
                print('m_totalQuantity = %d' % order.m_totalQuantity)
                print('m_orderType     = %s' % order.m_orderType)
            if 'contract' in self.con.order_dict[key]:
                contract = self.con.order_dict[key]['contract']
                print('contract        = %d' % contract.m_conId)

            print('status', ' ', self.con.order_dict[key]['status'])
            print('filled', ' ', self.con.order_dict[key]['filled'])
            print('permId', ' ', self.con.order_dict[key]['permId'])
            print('remaining', ' ', self.con.order_dict[key]['remaining'])
            print('avgFillPrice', ' ', self.con.order_dict[key]['avgFillPrice'])
            print('lastFillPrice', ' ', self.con.order_dict[key]['lastFillPrice'])
            print('whyHeld', ' ', self.con.order_dict[key]['whyHeld'])

        self.con.cancel_order(id1)
        time.sleep(0.2)
        self.con.get_open_orders()
        time.sleep(1)

        for key in self.con.order_dict:
            order = self.con.order_dict[key]['order']
            contract = self.con.order_dict[key]['contract']
            print('%s' % '-' * 60)
            print('m_orderId       = %d' % order.m_orderId)
            print('m_clientId      = %d' % order.m_clientId)
            print('m_permId        = %d' % order.m_permId)
            print('m_action        = %s' % order.m_action)
            print('m_totalQuantity = %d' % order.m_totalQuantity)
            print('m_orderType     = %s' % order.m_orderType)
            print('contract        = %d' % contract.m_conId)

        self.con.close()
        time.sleep(0.5)


if __name__ == "__main__":
    unittest.main()
