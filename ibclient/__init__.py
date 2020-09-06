import os
import sys
import platform

if sys.version_info < (3,):
    raise Exception("Python 2 has reached end-of-life and is no longer supported.")

__version__ = '0.0.3'
__author__ = 'Jin Xu'

__all__ = [

    "contract", "account", "utils", "IBClient", "Portfolio", "Account", "Position"
]

import ibclient.account
import ibclient.utils
import ibclient.contract

#
# """
# for IB client
# """
from ibclient.ib_client import (IBClient)

#
# """
# Account definitions
# """
from ibclient.account import (Portfolio, Account, Position)

from ibclient.orders import (OrderExecution, MarketOrder, LimitOrder)
from ibclient.contract import (new_contract, new_stock_contract,
                               new_futures_contract, new_option_contract,
                               )
