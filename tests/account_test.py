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

    def set_conn(self):
        con = IBClient(port=self.config['port'],
                       client_id=self.config['client_id'])
        con.connect()
        return con

    def test_acct(self):
        self.set_data()
        con = self.set_conn()

        context = Context()
        context.setup_account(self.config['account'],
                              starting_cash=self.config['starting_cash'])


        con.register_strategy(context, None)
        con.enable_account_info_update()
        
        for i in range(2):
            print(context.account)
            print('starting_cash   = %f' % context.portfolio.starting_cash     )
            print('capital_used    = %f' % context.portfolio.capital_used      )
            print('pnl             = %f' % context.portfolio.pnl               )
            print('portfolio_value = %f' % context.portfolio.portfolio_value   )
            print('positions_value = %f' % context.portfolio.positions_value   )
            print('returns         = %f' % context.portfolio.returns           )
            for sid in context.portfolio.positions:
                pos = context.portfolio.positions[sid]
                print('%s' % '-'*30)
                print('sid             = %f' %  pos.sid             )
                print('amount          = %f' %  pos.amount          )
                print('cost_basis      = %f' %  pos.cost_basis      )
                print('last_sale_price = %f' %  pos.last_sale_price )
                print('unrealized_pnl  = %f' %  pos.unrealized_pnl  )
                print('realized_pnl    = %f' %  pos.realized_pnl    )
            
            time.sleep(3)

        # TODO: add test logic here
        time.sleep(1)
        con.close()

if __name__ == "__main__":
    unittest.main()
