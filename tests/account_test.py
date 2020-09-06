# -*- coding:utf-8 -*-
'''
Test account, portfolio and position
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

    def tearDown(self):
        self.con.disconnect()

    def test01_acct(self):

        con = self.con
        con.setup_account(self.config['account'],
                          starting_cash=self.config['starting_cash'])

        con.enable_account_info_update()

        for i in range(2):
            print(con.account)
            print('starting_cash   = %f' % con.portfolio.starting_cash)
            print('capital_used    = %f' % con.portfolio.capital_used)
            print('pnl             = %f' % con.portfolio.pnl)
            print('portfolio_value = %f' % con.portfolio.portfolio_value)
            print('positions_value = %f' % con.portfolio.positions_value)
            print('returns         = %f' % con.portfolio.returns)
            for sid in con.portfolio.positions:
                pos = con.portfolio.positions[sid]
                print('%s' % '-' * 30)
                print('sid             = %f' % pos.sid)
                print('amount          = %f' % pos.amount)
                print('cost_basis      = %f' % pos.cost_basis)
                print('last_sale_price = %f' % pos.last_sale_price)
                print('unrealized_pnl  = %f' % pos.unrealized_pnl)
                print('realized_pnl    = %f' % pos.realized_pnl)

            time.sleep(3)


if __name__ == "__main__":
    unittest.main()
