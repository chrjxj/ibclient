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

