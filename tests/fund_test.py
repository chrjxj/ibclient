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
from ibclient import IBClient
from ibclient.orders_style import *
from ibclient.contract import new_stock_contract, new_futures_contract

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))
from tests.config import load_config


class Test(unittest.TestCase):

    def set_data(self):
        self.config = load_config('test-acc.yaml')
        pprint(self.config)

    def set_conn(self):
        con = IBClient(port=self.config['port'],
                       client_id=self.config['client_id'])
        con.connect()
        return con


class Test(unittest.TestCase):

    def set_data(self):
        self.config = load_config('test-acc.yaml')
        self.stock_symbol = self.config.get('stock_symbol_01', 'IBM')
        pprint(self.config)

    def set_conn(self):
        self.con = IBClient(port=self.config['port'],
                            client_id=self.config['client_id'])
        self.con.connect()
        return self.con

    def test001_ownership_report(self):
        print('test_ownership_report...')
        self.set_data()
        self.set_conn()

        max_wait_time = 60.
        status, data = self.con.get_company_ownership(self.stock_symbol, max_wait_time)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)

    def test002_finsmt_report(self):
        print('test_finsmt_report...')
        max_wait_time = 20.
        status, data = self.con.get_financial_statements(self.stock_symbol)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)

    def test003_analyst_report(self):
        print('test_analyst_report...')
        max_wait_time = 30.
        status, data = self.con.get_analyst_estimates(self.stock_symbol)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)

    def test004_financial_summary(self):
        print('test_financial_summary...')
        max_wait_time = 30.
        status, data = self.con.get_financial_summary(self.stock_symbol)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)

    def test005_company_overview(self):
        print('test_company_overview...')
        max_wait_time = 30.
        status, data = self.con.get_company_overview(self.stock_symbol)
        time.sleep(max_wait_time + 3)
        print(status)
        print(data)


if __name__ == "__main__":
    unittest.main()
