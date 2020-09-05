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
        print(60 * '-')
        pprint(self.config)
        _stock_config = self.config['stock']
        self.stock = new_stock_contract(_stock_config['symbol'],
                                        exchange=_stock_config['exchange'],
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
        time.sleep(0.5)

    def tearDown(self):
        self.con.disconnect()
        time.sleep(0.5)
        print(60 * '-')

    def test01_buy_stocks(self):
        id1 = self.con.order_amount(self.stock, 1000, style=MarketOrder())
        id2 = self.con.order_amount(self.stock, 1000, style=LimitOrder(20))
        time.sleep(0.5)
        print("order IDs: {}; {}".format(id1, id2))

    def test02_sell_stocks(self):
        id1 = self.con.order_amount(self.stock, -1000, style=MarketOrder())
        id2 = self.con.order_amount(self.stock, -1000, style=LimitOrder(20))

        print("order IDs: {}; {}".format(id1, id2))

    def test03_trade_futures(self):
        id1 = self.con.order_amount(self.future, 1, style=MarketOrder())
        id2 = self.con.order_amount(self.future, -1, style=LimitOrder(10000))


    def test04_trade_combo(self):
        time.sleep(0.5)


if __name__ == "__main__":
    unittest.main()
