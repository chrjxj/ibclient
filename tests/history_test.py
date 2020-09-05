# -*- coding:utf-8 -*-
'''
Created on 11/08/2016
@author: Jin Xu
'''
import sys
from os import path
import time
from pprint import pprint
import unittest
import datetime
import random

from ibclient import IBClient, new_stock_contract, new_futures_contract

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

    def test01_get_hist_data(self):

        print(self.con.get_price_history(self.stock, self.end, '3 D', 'daily'))
        print(self.con.get_price_history(self.future, self.end, '3 D', 'daily'))
        time.sleep(0.5)

    def test02_get_hist_data_long(self):
        print(self.con.get_price_history(self.stock, self.end, '3 M', 'daily'))
        self.con.close()
        time.sleep(0.5)

    def test03_get_realtime_price(self):
        id1, rt_p = self.con.request_realtime_price(self.stock)
        time.sleep(5)
        print(self.con.ipc_msg_dict[id1][1].rt_price)
        time.sleep(0.1)
        self.con.cancel_realtime_price(id1)
        time.sleep(0.5)


if __name__ == "__main__":
    unittest.main()
