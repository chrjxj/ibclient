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

    def test001_get_tick_snapshot(self):
        print('test_get_tick_snapshot...')
        self.set_data()
        self.set_conn()

        for i in range(20):
            try:
                tick_data = self.con.get_tick_snapshot(self.stock)
                time.sleep(10)
            except RuntimeError:
                self.con.close()
            else:
                print(tick_data)

        time.sleep(0.5)

    def test002_get_tick(self):
        print('def test_get_tick...')

        try:
            id2, tick_data = self.con.request_tick_data(self.stock)
            time.sleep(2)
        except RuntimeError:
            print('test_get_tick:RuntimeError')

        else:
            print(self.con.ipc_msg_dict[id2][1].tick_snapshot)
            time.sleep(5)
            print(self.con.ipc_msg_dict[id2][1].tick_snapshot)
            time.sleep(5)
            print(self.con.ipc_msg_dict[id2][1].tick_snapshot)
            time.sleep(5)
            self.con.cancel_tick_request(id2)
        self.con.close()
        time.sleep(0.5)


if __name__ == "__main__":
    unittest.main()
