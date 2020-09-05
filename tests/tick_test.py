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


    def test001_get_tick_snapshot(self):
        print('test_get_tick_snapshot...')

        for i in range(5):
            try:
                tick_data = self.con.get_tick_snapshot(self.stock)
                time.sleep(3)
            except RuntimeError:
                self.con.close()
            else:
                print(tick_data)

        time.sleep(0.5)

    def test002_get_tick(self):
        print('def test_get_tick...')

        try:
            id2, tick_data = self.con.request_tick_data(self.stock)
        except RuntimeError:
            print('test_get_tick:RuntimeError')

        else:
            print(self.con.ipc_msg_dict[id2][1].tick_data)
            time.sleep(2)
            print(self.con.ipc_msg_dict[id2][1].tick_data)
            time.sleep(2)
            print(self.con.ipc_msg_dict[id2][1].tick_data)
            time.sleep(2)
            self.con.cancel_tick_request(id2)
        self.con.close()
        time.sleep(0.5)

    def test003_get_market_depth(self):
        print('test003_get_market_depth...')

        try:
            id2, _data = self.con.request_market_depth(self.stock)
        except RuntimeError:
            print('test_get_tick:RuntimeError')
        else:
            for _ in range(10):
                print(_data)
                time.sleep(1)
            self.con.cancel_market_depth(id2)
        self.con.close()
        time.sleep(0.5)

if __name__ == "__main__":
    unittest.main()
