# coding=utf-8
from enum import Enum

# Tick Data Fields
TICK_FIELDS = {}
TICK_FIELDS[0] = 'bidVolume1'
TICK_FIELDS[1] = 'bidPrice1'
TICK_FIELDS[2] = 'askPrice1'
TICK_FIELDS[3] = 'askVolume1'
TICK_FIELDS[4] = 'lastPrice'
TICK_FIELDS[5] = 'lastVolume'
TICK_FIELDS[6] = 'highPrice'
TICK_FIELDS[7] = 'lowPrice'
TICK_FIELDS[8] = 'volume'
TICK_FIELDS[9] = 'preClosePrice'
TICK_FIELDS[14] = 'openPrice'
TICK_FIELDS[22] = 'openInterest'
TICK_FIELDS[45] = 'lastTradeTS'

# Define TICK_TYPE according to
# https://interactivebrokers.github.io/tws-api/tick_types.html
TICK_TYPE_001          = 1
TICK_TYPE_TIMESTAMP    = 45
TICK_TYPE_FIN_RATIOS   = 47
TICK_TYPE_DIVIDENDS    = 59
TICK_TYPE_NEWS         = 62

TICK_STRING_TYPES = [TICK_TYPE_TIMESTAMP, TICK_TYPE_FIN_RATIOS, TICK_TYPE_DIVIDENDS, TICK_TYPE_NEWS]

IB_FARM_NAME_LS = ('secdefhk', 'hkhmds', 'usfarm.us', 'jfarm', 'hfrarm', 'usfuture', 'usfuture.us',
                   'usfarm', 'ushmds', 'fundfarm', 'ilhmds', 'euhmds', 'mcgw1.ibllc.com.cn')


class TickType(Enum):
    TYPE_001     = 1
    TIMESTAMP    = 45
    FIN_RATIOS   = 47
    DIVIDENDS    = 59
    NEWS         = 62

    @staticmethod
    def values():
        return [member.value for name, member in TickType.__members__.items()]


class IBExchange(Enum):

    SMART = 'SMART'
    GLOBEX = 'GLOBEX'
    IDEALPRO = 'IDEALPRO'

    # North America
    NYMEX = 'NYMEX'
    NASDAQ = 'ISLAND'
    CFE = 'CFE'
    CBOE = 'CBOE'

    # Asia
    SGX = 'SGX'         # Singapore Exchange (SGX)
    SEHK = 'SEHK'       # Hong Kong Stock Exchange (SEHK)
    SEHKNTL = 'SEHKNTL' # 沪港通

    @staticmethod
    def values():
        return [member.value for name, member in IBExchange.__members__.items()]



class IBEXCHANGE(object):
    ''' Define exchange in IB system.
    Please refer to https://www.ibkr.com.cn/cn/index.php?f=5429 for details.
    For timezone strings, please refers to pytz.all_timezones
    A few commonly used timezone strings:
        'Asia/Bangkok',  'Asia/Dubai','Asia/Hong_Kong',  'Asia/Shanghai', 'Asia/Singapore',
        'US/Alaska',  'US/Central', 'US/Eastern', 'US/Mountain', 'US/Pacific', 'UTC',
    '''

    SMART = 'SMART'
    GLOBEX = 'GLOBEX'
    IDEALPRO = 'IDEALPRO'

    # North America
    NYMEX = 'NYMEX'
    NASDAQ = 'ISLAND'
    CFE = 'CFE'
    CBOE = 'CBOE'

    # Asia
    SGX = 'SGX'         # Singapore Exchange (SGX)
    SEHK = 'SEHK'       # Hong Kong Stock Exchange (SEHK)
    SEHKNTL = 'SEHKNTL' # 沪港通

    TIMEZONE = {}
    TIMEZONE['SGX'] = 'Asia/Shanghai'
    TIMEZONE['SEHK'] = 'Asia/Shanghai'
    TIMEZONE['SEHKNTL'] = 'Asia/Shanghai'
    TIMEZONE['NYMEX'] = 'US/Eastern'
    TIMEZONE['ISLAND'] = 'US/Eastern'
    TIMEZONE['NYMEX'] = 'US/Eastern'
    TIMEZONE['CFE'] = 'US/Central'
    TIMEZONE['CBOE'] = 'US/Central'
    TIMEZONE['SMART'] = 'US/Eastern'

    @staticmethod
    def get_timezone(exchange):
        return IBEXCHANGE.TIMEZONE.get(exchange, 'US/Eastern')



from datetime import datetime

class MarketDepth():
    """
    MarketDepth

    Sample data/message from TWS
            updateMktDepth 1000 0 1 1 24.45 765800
            updateMktDepth 1000 7 1 1 24.1 277000
            updateMktDepth 1000 0 1 0 24.5 368800
            updateMktDepth 1000 3 1 0 24.65 176000
            updateMktDepth 1000 4 1 0 24.7 302200
            updateMktDepth 1000 0 1 1 24.45 773400
            updateMktDepth 1000 1 1 1 24.4 1093000
            updateMktDepth 1000 0 1 0 24.5 365200
            updateMktDepth 1000 1 1 0 24.55 384400
            updateMktDepth 1000 3 1 0 24.65 173400
    """

    def __init__(self, request_id):
        self.__request_id = request_id
        self.last_update = datetime.now()
        self.__bid = [(-1, -1)] * 10
        self.__ask = [(-1, -1)] * 10

    def update(self, tickerId, position, operation, side, price, size):
        """
            see https://interactivebrokers.github.io/tws-api/market_depth.html#receive
        :param tickerId:
        :param position:
        :param operation: insert (0), update (1) or remove (2)
        :param side:
        :param price:
        :param size:
        :return:
        """
        assert tickerId == self.__request_id, "Invalid tickerId."
        assert position < 10, "Invalid position value."

        if side == 0:
            # ask side
            self.__ask[position] = (price, size)
        elif side == 1:
            self.__bid[position] = (price, size)
        else:
            raise ValueError

        self.last_update = datetime.now()


    def __str__(self):
        lines = ["\t\task\t\t\tbid"]
        for pos in range(10):
            lines.append("{}\t{}\t\t\t{}".format(pos, self.__ask[pos], self.__bid[pos]))

        return "\n".join(lines)

    def __repr__(self):
        lines = ["\t\task\t\t\tbid"]
        for pos in range(10):
            lines.append("{}\t{}\t\t\t{}".format(pos, self.__ask[pos], self.__bid[pos]))

        return "\n".join(lines)
