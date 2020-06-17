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

    def test01_buy_stocks(self):
        self.set_data()
        self.set_conn()
        id1 = self.con.order_amount(self.stock, 1000, style=MarketOrder())
        time.sleep(0.5)
        id2 = self.con.order_amount(new_stock_contract('DIN'), 1000, style=LimitOrder(8.6))

        time.sleep(0.5)

    def test02_sell_stocks(self):
        id1 = self.con.order_amount(self.stock, -500, style=MarketOrder())
        time.sleep(0.5)
        id2 = self.con.order_amount(new_stock_contract('DIN'), -500, style=LimitOrder(8.2))

        time.sleep(0.5)

    def test03_trade_futures(self):
        id1 = self.con.order_amount(self.future, 1, style=MarketOrder())
        time.sleep(0.5)
        id2 = self.con.order_amount(self.future, -1, style=LimitOrder(10000))
        time.sleep(0.5)

    def test04_trade_combo(self):
        time.sleep(0.5)
        self.con.close()
        time.sleep(0.5)


if __name__ == "__main__":
    unittest.main()
