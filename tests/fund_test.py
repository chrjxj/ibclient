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
import random
from pprint import pprint

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

    def test001_ownership_report(self):
        print('test_ownership_report...')

        max_wait_time = 60.
        status, data = self.con.get_company_ownership(self.stock, max_wait_time)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)

    def test002_finsmt_report(self):
        print('test_finsmt_report...')
        max_wait_time = 20.
        status, data = self.con.get_financial_statements(self.stock)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)

    def test003_analyst_report(self):
        print('test_analyst_report...')
        max_wait_time = 30.
        status, data = self.con.get_analyst_estimates(self.stock)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)

    def test004_financial_summary(self):
        print('test_financial_summary...')
        max_wait_time = 30.
        status, data = self.con.get_financial_summary(self.stock)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)

    def test005_company_overview(self):
        print('test_company_overview...')
        max_wait_time = 30.
        status, data = self.con.get_company_overview(self.stock)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)


if __name__ == "__main__":
    unittest.main()
