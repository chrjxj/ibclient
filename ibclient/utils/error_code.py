# coding=utf-8

'''
Define System Level Error Types
Created on 10/18/2016
@author: Jin Xu
@contact: jin_xu1@qq.com
'''


# Full API Message Codes
# https://www.interactivebrokers.com/en/software/api/apiguide/tables/api_message_codes.htm
#
# Some Sample Msg
#     farm_name, purpose, status
#     TWS Time at connection:20161129 13:01:53 CST
#     [TWS INFO]  Market data farm connection is OK:jfarm
#     [TWS INFO]  HMDS data farm connection is OK:hkhmds
#
#     [TWS INFO]  Market data farm connection is inactive but should be available upon demand.usfarm.us
#     [TWS INFO]  Market data farm connection is inactive but should be available upon demand.usfarm.us
#     [TWS INFO]  Market data farm connection is inactive but should be available upon demand.usfarm
#     [TWS INFO]  Market data farm connection is inactive but should be available upon demand.usfarm
#
#     TWS Time at connection:20161129 09:39:42 CST
#     [TWS INFO]  Market data farm connection is OK:hfarm
#     [TWS INFO]  Market data farm connection is OK:jfarm
#     [TWS INFO]  HMDS data farm connection is OK:ilhmds
#     error: -1 2105 HMDS data farm connection is broken:euhmds
#     [TWS INFO]  HMDS data farm connection is OK:hkhmds
#     [TWS INFO]  HMDS data farm connection is OK:ushmds
#     [TWS INFO]  HMDS data farm connection is OK:fundfarm
#     [ Tue Nov 29 09:39:41 2016 ] before_trading_start
#     error: 1 162 Historical Market Data Service error message:Trading TWS session is connected from a different IP address


class CodeMsgPair(object):
    """ Error Code and Msg """

    def __init__(self, error_code: int, error_msg: str):
        self.m_errorCode = error_code
        self.m_errorMsg = error_msg

    @property
    def code(self):
        """ generated source for method code """
        return self.m_errorCode

    @property
    def msg(self):
        """ generated source for method msg """
        return self.m_errorMsg



class IBSystemErrors(object):
    """ Define some common errors in socket and market data connections """
    NO_VALID_ID = -1
    TWS_CONN_LOST = CodeMsgPair(1100, "Connectivity between IB and the TWS has been lost.")
    TWS_RESTORED_LOD = CodeMsgPair(1101, "Connectivity between IB and TWS has been restored- data lost.*")
    TWS_RESTORED_MD = CodeMsgPair(1102, "Connectivity between IB and TWS has been restored- data maintained.")
    TWS_SOCKET_DROP = CodeMsgPair(1300, "TWS socket port has been reset and this connection is being dropped. Please reconnect on the new port - <port_num>")
    TWS_ACCT_DATA_LOSS = CodeMsgPair(2100, "New account data requested from TWS. API client has been unsubscribed from account data.")
    TWS_ACCT_DATA_ERR = CodeMsgPair(2101, "Unable to subscribe to account as the following clients are subscribed to a different account.")
    TWS_ORDER_ERR = CodeMsgPair(2102, "Unable to modify this order as it is still being processed.")
    TWS_MKT_DATA_DISCON = CodeMsgPair(2103, "A market data farm is disconnected.")
    TWS_MKT_DATA_OK = CodeMsgPair(2104, "Market data farm connection is OK")
    TWS_HIST_DATA_DISCON = CodeMsgPair(2105, "A historical data farm is disconnected.")
    TWS_HIST_DATA_OK = CodeMsgPair(2106, "A historical data farm is connected.")
    TWS_HIST_DATA_INACTIVE = CodeMsgPair(2107, "A historical data farm connection has become inactive but should be available upon demand.")
    TWS_MKT_DATA_INACTIVE = CodeMsgPair(2108, "A market data farm connection has become inactive but should be available upon demand.")
    TWS_ORDER_WARNING = CodeMsgPair(2109, "Order Event Warning: Attribute -Outside Regular Trading Hours- is ignored based on the order type and destination. PlaceOrder is now processed.")
    TWS_CONN_BROKEN = CodeMsgPair(2110, "Connectivity between TWS and server is broken. It will be restored automatically.")

