import os
import sys
import platform

if sys.version_info < (3,):
    raise Exception("Python 2 has reached end-of-life and is no longer supported.")

__version__ = '0.0.2'
__author__ = 'Jin Xu'

__all__ = [

"contract",    "account", "utils", "IBClient", "Context", "Portfolio", "Account", "Position"
]

import ibclient.account
import ibclient.utils
import ibclient.contract
import ibclient.orders_style

from ibclient.ib_client import (IBClient)

#
# """
# for IB client
# """
# from ibclient.ib_client import (IBClient)
#
# """
# for util functions
# """
# from ibclient.utils import *
#
# """
# for contract functions
# """
# from ibclient.contract import *
from ibclient.orders_style import *
#
# """
# Account definitions
# """
from ibclient.account import (Portfolio, Account, Position)
#
# """
# Context definitions
# """
from ibclient.context import (Context)
