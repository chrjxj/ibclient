# coding=utf-8
'''
Account, Portfolio, and Position
For simplicity, 1 Account : 1 Portfolio instance; 1 Portfolio : N Positions
Created on 11/21/2016
@author: Jin Xu
@contact: jin_xu1@qq.com
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import pandas as pd
import numpy as np
from ib.ext.Contract import Contract
from .account import Account
from .position import Position

class Portfolio(object):
    ''' Current assumption is 1 portfolio : 1 account.
    The portfolio object is accessed using  context.portfolio and has the following properties:
        capital_used
            Float: The net capital consumed (positive means spent) by buying and selling securities up to this point.cash
            Float: The current amount of cash in your portfolio.
        pnl
            Float: Dollar value profit and loss, for both realized and unrealized gains.
        positions
            Dictionary: A dictionary of all the open positions, keyed by security ID. More information about each position object can be found in
            the next section.
        portfolio_value
            Float: Sum value of all open positions and ending cash balance.
        positions_value
            Float: Sum value of all open positions.
        returns
            Float: Cumulative percentage returns for the entire portfolio up to this point. Calculated as a fraction of the starting value of the
            portfolio. The returns calculation includes cash and portfolio value. The number is not formatted as a percentage, so a 10% return is
            formatted as 0.1.
        starting_cash
            Float: Initial capital base for this backtest or live execution.start_date
    '''

    def __init__(self, account_id, starting_cash=1.):
        # the account this portfolio linked to
        self.account = Account(account_id)
        self.starting_cash = float(starting_cash)
        self.capital_used = float()
        self.pnl = float()
        self.positions = dict()
        # self.portfolio_value = self.account.net_liquidation
        # self.positions_value = self.account.total_positions_value
        self.returns = float()

    @property
    def portfolio_value(self):
        return self.account.net_liquidation

    @property
    def positions_value(self):
        return self.account.total_positions_value

    @property
    def cash(self):
        return self.account.excess_liquidity

    @property
    def leverage(self):
        return self.account.leverage

    #
    # def update(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL,
    #            accountName):
    #
    #     if not isinstance(contract, Contract):
    #         raise TypeError("contract must be a contract object")
    #
    #     # sid = (contract.m_conId, contract.m_symbol, contract.m_localSymbol)
    #     sid = contract.m_conId
    #     # TODO: use contract's unique ID as KEY
    #     if sid in self.positions:
    #         self.positions.pop(sid)
    #     self.positions[sid] = Position(sid, position, marketPrice, averageCost, unrealizedPNL, realizedPNL)
    #
    #     # sum all positions' value
    #     self.positions_value = 0.
    #     for sid in self.positions:
    #         p = self.positions[sid]
    #         self.positions_value += p.amount * p.last_sale_price
    #
    #     self.portfolio_value = self.positions_value + self.account.excess_liquidity
    #     self.pnl = self.portfolio_value - self.starting_cash
    #     assert (self.starting_cash != 0)
    #     self.returns = self.portfolio_value / self.starting_cash


    def update_positions(self, symbol, contract, position, marketPrice, marketValue, averageCost,
                         unrealizedPNL, realizedPNL, accountName):

        if not isinstance(contract, Contract):
            raise TypeError("contract must be a contract object")

        # sid = (contract.m_conId, contract.m_symbol, contract.m_localSymbol)
        sid = contract.m_conId

        self.positions[symbol] = Position(sid, position, marketPrice, averageCost, unrealizedPNL, realizedPNL)
        # updatePortfolio <ib.ext.Contract.Contract object at 0x0000000003EDD390> <class 'ib.ext.Contract.Contract'>
        # 4 10223.178711 10225.35 DU264039
        # calc
        # ['sid', 'amount', 'last_sale_price', 'cost_basis', 'unrealizedPNL', 'realizedPNL']

        # NOTE: out dated code; chagne to use the account member values instead;
        # # sum all positions' value
        # self.positions_value = 0.
        # for symbol in self.positions:
        #     p = self.positions[symbol]
        #     self.positions_value += p.amount * p.last_sale_price
        #
        # self.portfolio_value = self.positions_value + self.account.excess_liquidity

        # TODO: check the starting_cash
        self.pnl = self.portfolio_value - self.starting_cash
        assert (self.starting_cash != 0)
        self.returns = self.portfolio_value / self.starting_cash

    def print_summary(self):
        print('%s' % '-' * 60)
        print('portfolio_value            = %s' % (self.portfolio_value))
        print('positions_value            = %f' % (self.positions_value))
        print(Position.HEDAER)
        for symbol in self.positions:
            print('{} {}'.format(symbol, str(self.positions[symbol])))
        print('%s' % '-' * 60)
