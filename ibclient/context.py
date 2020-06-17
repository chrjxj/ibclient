# coding=utf-8

'''
Account, Portfolio, and Position
For simplicity, 1 Account : 1 Portfolio instance; 1 Portfolio : N Positions
Created on 11/21/2016
@author: Jin Xu
@contact: jin_xu1@qq.com
'''
from __future__ import absolute_import, print_function, division
import pandas as pd
from datetime import datetime
from .account import Portfolio
from .contract import new_stock_contract


class Context(object):
    def __init__(self):
        # Setup time related variables

        now = datetime.now()
        self.year = now.year
        self.month = now.month
        self.day = now.day
        self.universe = []
        # setup thread pool
        self.threads = []

        self.symbol_db = dict()
        self.symbol_conid_tbl = dict()
        # setup later
        self.portfolio = None
        self.account = None

    def setup_account(self, account_id, starting_cash):
        self.portfolio = Portfolio(account_id, starting_cash)
        self.account = self.portfolio.account

    def init_symbol_db(self, db_file):


        df = pd.read_csv(db_file, dtype={'Symbol': str, 'Name': str, 'Exchange': str, 'Type': str, 'Currency': str,
                                         'Conid': int})

        # for symbol in context.contract_lib_df.index.tolist():
        for idx, row in df.iterrows():
            if str(row['Type']).lower() == "stock":
                contract = new_stock_contract(row['Symbol'], exchange=row['Exchange'],
                                              primary_exchange=row['Exchange'], currency=row['Currency'],
                                              contract_id=int(row['Conid']))
            else:
                raise NotImplementedError

            self.symbol_db[row['Symbol']] = dict(symbol=row['Symbol'], name=row['Name'],
                                                 type=row['Type'], contract=contract, conid=row['Conid'])
            self.symbol_conid_tbl[int(row['Conid'])] = row['Symbol']

    def get_symbol_by_conid(self, conid):
        assert (isinstance(conid, int))
        return self.symbol_conid_tbl.get(conid)

