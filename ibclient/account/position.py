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

class Position(object):
    '''
    The position object represents a current open position, and is contained inside the positions dictionary. For example, if you had an open
    AAPL position, you'd access it using  context.portfolio.positions[symbol('AAPL')]. The position object has the following properties:
    amount
    Integer: Whole number of shares in this position.
    cost_basis
    Float: The volume-weighted average price paid (price and commission) per share in this position.
    last_sale_price
    Float: Price at last sale of this security. This is identical to  close_price and  price.
    sid
    Integer: The ID of the security.
    '''

    HEADER = "\tlast_price\tamount\t\tavg_cost\t\tunrealized_pnl\t\trealized_pnl"

    def __init__(self, sid, amount, last_sale_price, cost_basis, unrealizedPNL, realizedPNL):
        self.amount = int(amount)
        self.cost_basis = float(cost_basis)
        self.last_sale_price = float(last_sale_price)
        self.sid = int(sid)
        self.unrealized_pnl = float(unrealizedPNL)
        self.realized_pnl = float(realizedPNL)

    def __str__(self):
        return "\t%.2f\t\t%d\t\t%.2f\t\t%.2f\t\t%.2f\n" % (self.last_sale_price, self.amount, self.cost_basis,
                                                           self.unrealized_pnl, self.realized_pnl)

    def __repr__(self):
        return "\t%.2f\t\t%d\t\t%.2f\t\t%.2f\t\t%.2f\n" % (self.last_sale_price, self.amount, self.cost_basis,
                                                           self.unrealized_pnl, self.realized_pnl)
