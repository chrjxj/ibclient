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


class Account(object):
    '''
        Below is a table of account fields available to reference in a live trading algorithm with Interactive Brokers.
        context.account.accrued_interest (IB: AccruedCash)
        (Float) Interest that has accumulated but has not been paid or charged.
        (Float) Equity with loan value less the initial margin requirement.
        context.account.buying_power (IB: BuyingPower)
        (Float)
        IB Cash Account: Minimum (Equity with Loan Value, Previous Day Equity with Loan Value)-Initial Margin.
        IB Margin Account: Available Funds * 4.
        context.account.cushion (IB: Cushion)
        (Float) Excess liquidity as a percentage of net liquidation.
        context.account.day_trades_remaining (IB: DayTradesRemaining)
        (Float) The number of open/close trades a user can place before pattern day trading is detected.
        context.account.equity_with_loan (IB: EquityWithLoanValue)
        (Float)
        IB Cash Account: Settled Cash.
        IB Margin Account: Total cash value + stock value + bond value + (non-U.S. & Canada securities options value).
        context.account.excess_liquidity (IB: ExcessLiquidity)
        (Float) Equity with loan value less the maintenance margin.Backtest value:  context.portfolio.cash
        context.account.initial_margin_requirement (IB: InitMarginReq)
        (Float) The minimum portion of a new security purchase that an investor must pay for in cash.
        context.account.leverage (IB: GrossLeverage)
        (Float) Gross position value divided by net liquidation.
        context.account.maintenance_margin_requirement (IB: MaintMarginReq)
        (Float) The amount of equity which must be maintained in order to continue holding a position.
        context.account.net_leverage (IB: NetLeverage)
        (Float) The default value is also used for live trading.
        context.account.net_liquidation (IB: NetLiquidation)
        (Float) Total cash, stock, securities options, bond, and fund value.
        context.account.regt_equity (IB: RegTEquity)
        (Float)
        IB Cash Account: Settled Cash.IB Margin Account: Total cash value + stock value + bond value + (non-U.S. & Canada securities options value).
        context.account.regt_margin (IB: RegTMargin)
        (Float) The margin requirement calculated under US Regulation T rules.
        context.account.settled_cash (IB: SettledCash)
        (Float) Cash recognized at the time of settlement less purchases at the time of trade, commissions, taxes, and fees.
        context.account.total_positions_value (IB: GrossPositionValue)
        (Float) The sum of the absolute value of all stock and equity option positions.
    '''

    KEYS = ['AvailableFunds', 'AccruedCash', 'BuyingPower', 'Cushion', 'EquityWithLoanValue',
            'ExcessLiquidity', 'InitMarginReq', 'MaintMarginReq', 'NetLiquidation', 'RegTEquity',
            'RegTMargin', 'SettledCash', 'GrossPositionValue']

    def __init__(self, account_id):
        self.account_id = account_id
        self.account_currency = ''
        self.accrued_interest = 0.
        self.buying_power = 0.
        self.cushion = 0.
        self.day_trades_remaining = 0.
        self.equity_with_loan = 0.
        self.excess_liquidity = 0.
        self.initial_margin_requirement = 0.
        self.leverage = 0.
        self.maintenance_margin_requirement = 0.
        self.net_leverage = 0.
        self.net_liquidation = 0.
        self.regt_equity = 0.
        self.regt_margin = 0.
        self.settled_cash = 0.
        self.total_positions_value = 0.
        self.available_fund = 0.

    def update(self, key, value, currency, account_id):
        # key, value, currency, accountName
        self.account_currency = currency
        if account_id != self.account_id:
            print('Received incorrect IB account ID')
            return

        if key == 'AvailableFunds':      self.available_fund = float(value)
        if key == 'AccruedCash':         self.accrued_interest = float(value)
        if key == 'BuyingPower':         self.buying_power = float(value)
        if key == 'Cushion':             self.cushion = float(value)
        if key == 'EquityWithLoanValue': self.equity_with_loan = float(value)
        if key == 'ExcessLiquidity':     self.excess_liquidity = float(value)
        if key == 'InitMarginReq':       self.initial_margin_requirement = float(value)
        if key == 'MaintMarginReq':      self.maintenance_margin_requirement = float(value)
        if key == 'NetLiquidation':      self.net_liquidation = float(value)
        if key == 'RegTEquity':          self.regt_equity = float(value)
        if key == 'RegTMargin':          self.regt_margin = float(value)
        if key == 'SettledCash':         self.settled_cash = float(value)
        if key == 'GrossPositionValue':  self.total_positions_value = float(value)

        # GrossLeverage (Float) Gross position value divided by net liquidation.
        if self.net_liquidation != 0.:
            self.leverage = self.total_positions_value / self.net_liquidation
        else:
            self.leverage = 0.
        # if key == '':         self.day_trades_remaining            = float(value)
        # if key == '':         self.net_leverage    = float(value)

    def __str__(self):

        return '\n'.join([
            '%s' % '-' * 60,
            'account_id                      = {}'.format(self.account_id),
            'accrued_interest                = {:.2f}'.format(self.accrued_interest),
            'buying_power                    = {:.2f}'.format(self.buying_power),
            'cushion                         = {:.2f}'.format(self.cushion),
            'day_trades_remaining            = {:.2f}'.format(self.day_trades_remaining),
            'equity_with_loan                = {:.2f}'.format(self.equity_with_loan),
            'excess_liquidity                = {:.2f}'.format(self.excess_liquidity),
            'initial_margin_requirement      = {:.2f}'.format(self.initial_margin_requirement),
            'leverage                        = {:.2f}'.format(self.leverage),
            'maintenance_margin_requirement  = {:.2f}'.format(self.maintenance_margin_requirement),
            'net_leverage                    = {:.2f}'.format(self.net_leverage),
            'net_liquidation                 = {:.2f}'.format(self.net_liquidation),
            'regt_equity                     = {:.2f}'.format(self.regt_equity),
            'regt_margin                     = {:.2f}'.format(self.regt_margin),
            'settled_cash                    = {:.2f}'.format(self.settled_cash),
            'total_positions_value           = {:.2f}'.format(self.total_positions_value),
            '%s' % '-' * 60,
        ])

    def __repr__(self):
        return '\n'.join([
            '%s' % '-' * 60,
            'account_id                      = {}'.format(self.account_id),
            'accrued_interest                = {:.2f}'.format(self.accrued_interest),
            'buying_power                    = {:.2f}'.format(self.buying_power),
            'cushion                         = {:.2f}'.format(self.cushion),
            'day_trades_remaining            = {:.2f}'.format(self.day_trades_remaining),
            'equity_with_loan                = {:.2f}'.format(self.equity_with_loan),
            'excess_liquidity                = {:.2f}'.format(self.excess_liquidity),
            'initial_margin_requirement      = {:.2f}'.format(self.initial_margin_requirement),
            'leverage                        = {:.2f}'.format(self.leverage),
            'maintenance_margin_requirement  = {:.2f}'.format(self.maintenance_margin_requirement),
            'net_leverage                    = {:.2f}'.format(self.net_leverage),
            'net_liquidation                 = {:.2f}'.format(self.net_liquidation),
            'regt_equity                     = {:.2f}'.format(self.regt_equity),
            'regt_margin                     = {:.2f}'.format(self.regt_margin),
            'settled_cash                    = {:.2f}'.format(self.settled_cash),
            'total_positions_value           = {:.2f}'.format(self.total_positions_value),
            '%s' % '-' * 60,
        ])
