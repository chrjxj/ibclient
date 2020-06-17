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

from ibclient import *
from ibclient import IBClient
from ibclient.orders_style import *
from ibclient.contract import new_stock_contract, new_futures_contract

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))
from tests.config import load_config


class Test(unittest.TestCase):

    def set_data(self):
        self.config = load_config('test-acc.yaml')
        pprint(self.config)

        self.stock = new_stock_contract(self.config.get('stock_symbol_01', 'IBM'))
        self.stock_str = self.config.get('stock_symbol_02', 'DIN')

        self.future = new_futures_contract(self.config['symbol'],
                                           self.config['exchange'],
                                           False,
                                           expiry=str(self.config['expiry']),
                                           tradingClass=self.config['tradingClass'])
        self.end = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')

    def set_conn(self):
        self.con = IBClient(port=self.config['port'],
                            client_id=self.config['client_id'])
        self.con.connect()
        return self.con

    def test01_get_open_orders(self):
        print('%s test_get_open_orders %s' % ('-' * 30, '-' * 30))
        self.set_data()
        self.set_conn()
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
