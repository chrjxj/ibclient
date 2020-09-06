﻿# coding=utf-8

'''
Define System Level Error Types
Created on 10/18/2016
@author: Jin Xu
@contact: jin_xu1@qq.com
'''


# Full API Message Codes
# https://interactivebrokers.github.io/tws-api/message_codes.html
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
    TWS_SOCKET_DROP = CodeMsgPair(1300,
                                  "TWS socket port has been reset and this connection is being dropped. Please reconnect on the new port - <port_num>")
    TWS_ACCT_DATA_LOSS = CodeMsgPair(2100,
                                     "New account data requested from TWS. API client has been unsubscribed from account data.")
    TWS_ACCT_DATA_ERR = CodeMsgPair(2101,
                                    "Unable to subscribe to account as the following clients are subscribed to a different account.")
    TWS_ORDER_ERR = CodeMsgPair(2102, "Unable to modify this order as it is still being processed.")
    TWS_MKT_DATA_DISCON = CodeMsgPair(2103, "A market data farm is disconnected.")
    TWS_MKT_DATA_OK = CodeMsgPair(2104, "Market data farm connection is OK")
    TWS_HIST_DATA_DISCON = CodeMsgPair(2105, "A historical data farm is disconnected.")
    TWS_HIST_DATA_OK = CodeMsgPair(2106, "A historical data farm is connected.")
    TWS_HIST_DATA_INACTIVE = CodeMsgPair(2107,
                                         "A historical data farm connection has become inactive but should be available upon demand.")
    TWS_MKT_DATA_INACTIVE = CodeMsgPair(2108,
                                        "A market data farm connection has become inactive but should be available upon demand.")
    TWS_ORDER_WARNING = CodeMsgPair(2109,
                                    "Order Event Warning: Attribute -Outside Regular Trading Hours- is ignored based on the order type and destination. PlaceOrder is now processed.")
    TWS_CONN_BROKEN = CodeMsgPair(2110,
                                  "Connectivity between TWS and server is broken. It will be restored automatically.")


TWSMessage = {

    1100: "Connectivity between IB and the TWS has been lost.",
    1101: "Connectivity between IB and TWS has been restored- data lost.*",
    1102: "Connectivity between IB and TWS has been restored- data maintained.",
    1300: "TWS socket port has been reset and this connection is being dropped. Please reconnect on the new port - <port_num>",
}

WarningMessage = {

    2100: "New account data requested from TWS. API client has been unsubscribed from account data.",
    2101: "Unable to subscribe to account as the following clients are subscribed to a different account.",
    2102: "Unable to modify this order as it is still being processed.",
    2103: "A market data farm is disconnected.",
    2104: "Market data farm connection is OK",
    2105: "A historical data farm is disconnected.",
    2106: "A historical data farm is connected.",
    2107: "A historical data farm connection has become inactive but should be available upon demand.",
    2108: "A market data farm connection has become inactive but should be available upon demand.",
    2109: "Order Event Warning: Attribute -Outside Regular Trading Hours- is ignored based on the order type and destination. PlaceOrder is now processed.",
    2110: "Connectivity between TWS and server is broken. It will be restored automatically.",
}

ClientError = {
    501: "Already Connected.",
    502: "Couldn't connect to TWS. Confirm that `Enable ActiveX and Socket Clients` is enabled.",
    503: "The TWS is out of date and must be upgraded.",
    504: "Not connected.",
}

TWSError = {
    100: "Max rate of messages per second has been exceeded.",
    101: "Max number of tickers has been reached.",
    102: "Duplicate ticker ID.",
    103: "Duplicate order ID.",
    104: "Cant modify a filled order.",
    105: "Order being modified does not match original order.",
    106: "Cant transmit order ID:",
    107: "Cannot transmit incomplete order.",
    109: "Price is out of the range defined by the Percentage setting at order defaults frame. The order will not be transmitted.",
    110: "The price does not conform to the minimum price variation for this contract.",
    111: "The TIF (Tif type) and the order type are incompatible.",
    113: "The Tif option should be set to DAY for MOC and LOC orders.",
    114: "Relative orders are valid for stocks only.",
    115: "Relative orders for US stocks can only be submitted to SMART, SMART_ECN, INSTINET, or PRIMEX.",
    116: "The order cannot be transmitted to a dead exchange.",
    117: "The block order size must be at least 50.",
    118: "VWAP orders must be routed through the VWAP exchange.",
    119: "Only VWAP orders may be placed on the VWAP exchange.",
    120: "It is too late to place a VWAP order for today.",
    121: "Invalid BD flag for the order. Check Destination and BD flag.",
    122: "No request tag has been found for order:",
    123: "No record is available for conid:",
    124: "No market rule is available for conid:",
    125: "Buy price must be the same as the best asking price.",
    126: "Sell price must be the same as the best bidding price.",
    129: "VWAP orders must be submitted at least three minutes before the start time.",
    131: "The sweep-to-fill flag and display size are only valid for US stocks routed through SMART, and will be ignored.",
    132: "This order cannot be transmitted without a clearing account.",
    133: "Submit new order failed.",
    134: "Modify order failed.",
    135: "Cant find order with ID =",
    136: "This order cannot be cancelled.",
    137: "VWAP orders can only be cancelled up to three minutes before the start time.",
    138: "Could not parse ticker request:",
    139: "Parsing error:",
    140: "The size value should be an integer:",
    141: "The price value should be a double:",
    142: "Institutional customer account does not have account info",
    143: "Requested ID is not an integer number.",
    144: "Order size does not match total share allocation.",
    145: "Error in validating entry fields -",
    146: "Invalid trigger method.",
    147: "The conditional contract info is incomplete.",
    148: "A conditional order can only be submitted when the order type is set to limit or market.",
    151: "This order cannot be transmitted without a user name.",
    152: "The hidden order attribute may not be specified for this order.",
    153: "EFPs can only be limit orders.",
    154: "Orders cannot be transmitted for a halted security.",
    155: "A sizeOp order must have a user name and account.",
    156: "A SizeOp order must go to IBSX",
    157: "An order can be EITHER Iceberg or Discretionary. Please remove either the Discretionary amount or the Display size.",
    158: "You must specify an offset amount or a percent offset value.",
    159: "The percent offset value must be between 0% and 100%.",
    160: "The size value cannot be zero.",
    161: "Cancel attempted when order is not in a cancellable state. Order permId =",
    162: "Historical market data Service error message.",
    163: "The price specified would violate the percentage constraint specified in the default order settings.",
    164: "There is no market data to check price percent violations.",
    165: "Historical market Data Service query message.",
    166: "HMDS Expired Contract Violation.",
    167: "VWAP order time must be in the future.",
    168: "Discretionary amount does not conform to the minimum price variation for this contract.",
    200: "No security definition has been found for the request.",
    201: "Order rejected - Reason:",
    202: "Order cancelled - Reason:",
    203: "The security <security> is not available or allowed for this account.",
    300: "Cant find EId with ticker Id:",
    301: "Invalid ticker action:",
    302: "Error parsing stop ticker string:",
    303: "Invalid action:",
    304: "Invalid account value action:",
    305: "Request parsing error, the request has been ignored.",
    306: "Error processing DDE request:",
    307: "Invalid request topic:",
    308: "Unable to create the API page in TWS as the maximum number of pages already exists.",
    309: "Max number (3) of market depth requests has been reached. ",
    310: "Cant find the subscribed market depth with tickerId:",
    311: "The origin is invalid.",
    312: "The combo details are invalid.",
    313: "The combo details for leg <leg number> are invalid.",
    314: "Security type BAG requires combo leg details.",
    315: "Stock combo legs are restricted to SMART order routing.",
    316: "Market depth data has been HALTED. Please re-subscribe.",
    317: "Market depth data has been RESET. Please empty deep book contents before applying any new entries.",
    319: "Invalid log level <log level>",
    320: "Server error when reading an API client request.",
    321: "Server error when validating an API client request.",
    322: "Server error when processing an API client request.",
    323: "Server error: cause - s",
    324: "Server error when reading a DDE client request (missing information).",
    325: "Discretionary orders are not supported for this combination of exchange and order type.",
    326: "Unable to connect as the client id is already in use. Retry with a unique client id.",
    327: "Only API connections with clientId set to 0 can set the auto bind TWS orders property.",
    328: "Trailing stop orders can be attached to limit or stop-limit orders only.",
    329: "Order modify failed. Cannot change to the new order type.",
    330: "Only FA or STL customers can request managed accounts list.",
    331: "Internal error. FA or STL does not have any managed accounts.",
    332: "The account codes for the order profile are invalid.",
    333: "Invalid share allocation syntax.",
    334: "Invalid Good Till Date order",
    335: "Invalid delta: The delta must be between 0 and 100.",
    336: "The time or time zone is invalid. ",
    337: "The date, time, or time-zone entered is invalid. The correct format is yyyymmdd hh:mm:ss xxx ",
    338: "Good After Time orders are currently disabled on this exchange.",
    339: "Futures spread are no longer supported. Please use combos instead.",
    340: "Invalid improvement amount for box auction strategy.",
    341: "Invalid delta. Valid values are from 1 to 100. ",
    342: "Pegged order is not supported on this exchange.",
    343: "The date, time, or time-zone entered is invalid. The correct format is yyyymmdd hh:mm:ss xxx",
    344: "The account logged into is not a financial advisor account.",
    345: "Generic combo is not supported for FA advisor account.",
    346: "Not an institutional account or an away clearing account.",
    347: "Short sale slot value must be 1 (broker holds shares) or 2 (delivered from elsewhere).",
    348: "Order not a short sale – type must be SSHORT to specify short sale slot.",
    349: "Generic combo does not support Good After attribute.",
    350: "Minimum quantity is not supported for best combo order.",
    351: "The Regular Trading Hours only flag is not valid for this order.",
    352: "Short sale slot value of 2 (delivered from elsewhere) requires location.",
    353: "Short sale slot value of 1 requires no location be specified.",
    354: "Not subscribed to requested market data.",
    355: "Order size does not conform to market rule.",
    356: "Smart-combo order does not support OCA group.",
    357: "Your client version is out of date.",
    358: "Smart combo child order not supported.",
    359: "Combo order only supports reduce on fill without block(OCA).",
    360: "No whatif check support for smart combo order.",
    361: "Invalid trigger price.",
    362: "Invalid adjusted stop price.",
    363: "Invalid adjusted stop limit price.",
    364: "Invalid adjusted trailing amount.",
    365: "No scanner subscription found for ticker id:",
    366: "No historical data query found for ticker id:",
    367: "Volatility type if set must be 1 or 2 for VOL orders. Do not set it for other order types.",
    368: "Reference Price Type must be 1 or 2 for dynamic volatility management. Do not set it for non-VOL orders.",
    369: "Volatility orders are only valid for US options.",
    370: "Dynamic Volatility orders must be SMART routed, or trade on a Price Improvement Exchange.",
    371: "VOL order requires positive floating point value for volatility. Do not set it for other order types.",
    372: "Cannot set dynamic VOL attribute on non-VOL order.",
    373: "Can only set stock range attribute on VOL or RELATIVE TO STOCK order.",
    374: "If both are set, the lower stock range attribute must be less than the upper stock range attribute.",
    375: "Stock range attributes cannot be negative.",
    376: "The order is not eligible for continuous update. The option must trade on a cheap-to-reroute exchange.",
    377: "Must specify valid delta hedge order aux. price.",
    378: "Delta hedge order type requires delta hedge aux. price to be specified.",
    379: "Delta hedge order type requires that no delta hedge aux. price be specified.",
    380: "This order type is not allowed for delta hedge orders.",
    381: "Your DDE.dll needs to be upgraded.",
    382: "The price specified violates the number of ticks constraint specified in the default order settings.",
    383: "The size specified violates the size constraint specified in the default order settings.",
    384: "Invalid DDE array request.",
    385: "Duplicate ticker ID for API scanner subscription.",
    386: "Duplicate ticker ID for API historical data query.",
    387: "Unsupported order type for this exchange and security type.",
    388: "Order size is smaller than the minimum requirement.",
    389: "Supplied routed order ID is not unique.",
    390: "Supplied routed order ID is invalid.",
    391: "The time or time-zone entered is invalid. The correct format is hh:mm:ss xxx",
    392: "Invalid order: contract expired.",
    393: "Short sale slot may be specified for delta hedge orders only.",
    394: "Invalid Process Time: must be integer number of milliseconds between 100 and 2000. Found:",
    395: "Due to system problems, orders with OCA groups are currently not being accepted.",
    396: "Due to system problems, application is currently accepting only Market and Limit orders for this contract.",
    397: "Due to system problems, application is currently accepting only Market and Limit orders for this contract.",
    398: "< > cannot be used as a condition trigger.",
    399: "Order message error",
    400: "Algo order error.",
    401: "Length restriction.",
    402: "Conditions are not allowed for this contract.",
    403: "Invalid stop price.",
    404: "Shares for this order are not immediately available for short sale. The order will be held while we attempt to locate the shares.",
    405: "The child order quantity should be equivalent to the parent order size.",
    406: "The currency < > is not allowed.",
    407: "The symbol should contain valid non-unicode characters only.",
    408: "Invalid scale order increment.",
    409: "Invalid scale order. You must specify order component size.",
    410: "Invalid subsequent component size for scale order.",
    411: "The Outside Regular Trading Hours flag is not valid for this order.",
    412: "The contract is not available for trading.",
    413: "What-if order should have the transmit flag set to true.",
    414: "Snapshot market data subscription is not applicable to generic ticks.",
    415: "Wait until previous RFQ finishes and try again.",
    416: "RFQ is not applicable for the contract. Order ID:",
    417: "Invalid initial component size for scale order.",
    418: "Invalid scale order profit offset.",
    419: "Missing initial component size for scale order.",
    420: "Invalid real-time query.",
    421: "Invalid route.",
    422: "The account and clearing attributes on this order may not be changed.",
    423: "Cross order RFQ has been expired. THI committed size is no longer available. Please open order dialog and verify liquidity allocation.",
    424: "FA Order requires allocation to be specified.",
    425: "FA Order requires per-account manual allocations because there is no common clearing instruction. Please use order dialog Adviser tab to enter the allocation.",
    426: "None of the accounts have enough shares.",
    427: "Mutual Fund order requires monetary value to be specified.",
    428: "Mutual Fund Sell order requires shares to be specified.",
    429: "Delta neutral orders are only supported for combos (BAG security type).",
    430: "We are sorry, but fundamentals data for the security specified is not available.",
    431: "What to show field is missing or incorrect.",
    432: "Commission must not be negative.",
    433: "Invalid Restore size after taking profit for multiple account allocation scale order.",
    434: "The order size cannot be zero.",
    435: "You must specify an account.",
    436: "You must specify an allocation (either a single account, group, or profile).",
    437: "Order can have only one flag Outside RTH or Allow PreOpen.",
    438: "The application is now locked.",
    439: "Order processing failed. Algorithm definition not found.",
    440: "Order modify failed. Algorithm cannot be modified.",
    441: "Algo attributes validation failed:",
    442: "Specified algorithm is not allowed for this order.",
    443: "Order processing failed. Unknown algo attribute.",
    444: "Volatility Combo order is not yet acknowledged. Cannot submit changes at this time.",
    445: "The RFQ for this order is no longer valid.",
    446: "Missing scale order profit offset.",
    447: "Missing scale price adjustment amount or interval.",
    448: "Invalid scale price adjustment interval.",
    449: "Unexpected scale price adjustment amount or interval.",
    507: "Bad Message Length (Java-only)",
    10000: "Cross currency combo error.",
    10001: "Cross currency vol error.",
    10002: "Invalid non-guaranteed legs.",
    10003: "IBSX not allowed.",
    10005: "Read-only models.",
    10006: "Missing parent order.",
    10007: "Invalid hedge type.",
    10008: "Invalid beta value.",
    10009: "Invalid hedge ratio.",
    10010: "Invalid delta hedge order.",
    10011: "Currency is not supported for Smart combo.",
    10012: "Invalid allocation percentage",
    10013: "Smart routing API error (Smart routing opt-out required).",
    10014: "PctChange limits.",
    10015: "Trading is not allowed in the API.",
    10016: "Contract is not visible.",
    10017: "Contracts are not visible.",
    10018: "Orders use EV warning.",
    10019: "Trades use EV warning.",
    10020: "Display size should be smaller than order size./td>",
    10021: "Invalid leg2 to Mkt Offset API.",
    10022: "Invalid Leg Prio API.",
    10023: "Invalid combo display size API.",
    10024: "Invalid dont start next legin API.",
    10025: "Invalid leg2 to Mkt time1 API.",
    10026: "Invalid leg2 to Mkt time2 API.",
    10027: "Invalid combo routing tag API.",
    10090: "Part of requested market data is not subscribed.",
    10148: "OrderId <OrderId> that needs to be cancelled can not be cancelled, state:",
    10186: "Requested market data is not subscribed. Delayed market data is not enabled18.0pt;padding-bottom:2px;padding-top:",
}
