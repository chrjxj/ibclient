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

from ibclient import IBClient
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

    def test01_get_hist_data(self):
        self.set_data()

        print(self.con.get_price_history(self.stock, self.end, '3 D', 'daily'))
        print(self.con.get_price_history(self.stock_str, self.end, '10 D', 'minute'))
        print(self.con.get_price_history(self.future, self.end, '3 D', 'daily'))

        time.sleep(0.5)

    def test02_get_hist_data_long(self):
        print(self.con.get_price_history(self.stock, self.end, '3 M', 'daily'))
        print(self.con.get_price_history(self.stock_str, self.end, '1 Y', 'daily'))
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
