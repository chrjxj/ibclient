# encoding: UTF-8

'''
IB Socket Client
Created on 10/18/2016
@author: Jin Xu
@contact: jin_xu1@qq.com
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import datetime as datetime
from copy import copy
import threading
from threading import Event
from time import sleep
import pandas as pd
from ib.ext.Order import Order
from ib.ext.EClientSocket import EClientSocket

from ibclient.msg_wrapper import IBMsgWrapper
from ibclient.utils import (RequestDetails,
                    ResponseDetails)

from ibclient.parsers import (parse_ownership_report,
                      parse_analyst_estimates,
                      parse_fin_statements)

from .constants import IB_FARM_NAME_LS
from .orders_style import *
from .contract import *

class IBClient(object):
    """IB Socket client"""

    def __init__(self, host='localhost', port=7496, client_id=0, client_name='IB'):
        """

        Args:
            host: TWS 所在机器的 IP或域名
            port: TWS配置的接收外部API的端口.TWS default value: 7496; TWS demo account default value: 7497
            client_id: API<->TWS之间 sock连接的ID
            client_name: 本次连接的名字。可选
        """


        self.client_name = client_name
        self.host = host  # host IP address in a string; e.g. '127.0.0.1', 'localhost'
        self.port = port  # socket port;
        self.client_id = client_id  # socket client id

        self.connected = False  # status of the socket connection

        self.tickerId = 0  # known as ticker ID or request ID
        self.ipc_msg_dict = {}  # key: ticker ID or request ID; value: request and response objects; response objects ususally carrys data, Events, and Status
        self.order_id = 0  # current available order ID
        self.order_dict = {}  # key: ticker ID or request ID; value: request and response objects; response objects ususally carrys data, Events, and Status

        self.context = None  # key: ticker ID or request ID; value: request and response objects; response objects ususally carrys data, Events, and Status

        self.wrapper = IBMsgWrapper(self)  # the instance with IB message callback methods
        self.connection = EClientSocket(self.wrapper)  # low layer socket client

        # TWS's data connection status
        self.hmdf_status_dict = {}
        for farm in IB_FARM_NAME_LS:
            self.hmdf_status_dict[farm] = 'unknown'

        # EVENTS
        self.conn_down_event = Event()  # sock connection event
        self.mdf_conn_event = Event()  # market data connection event
        self.hdf_conn_event = Event()  # hist data connection event

        self.order_event = Event()
        self.account_event = Event()
        self.get_order_event = Event()

        # LOCKER
        self.req_id_locker = threading.Lock()

        # CONSTANT VALUES
        self.PRICE_DF_HEADER1 = ['time', 'open', 'high', 'low', 'close', 'volume']
        self.PRICE_DF_HEADER2 = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']

    def connect(self):
        """ Connect to socket host, e.g. TWS """
        self.connection.eConnect(self.host, self.port, self.client_id)

        timeout = 5.
        count = 0.
        while not self.connected and count < timeout:
            count += 0.05
            sleep(0.05)

        if self.connected:
            self.order_id = self.connection.reqIds(-1)
            if self.context is not None:
                # TODO: may need to move this to a thread or at user layer
                self.enable_account_info_update()
        else:
            print('failed to connect.')

        return self.connected

    def close(self):
        """ disconnect from IB host """
        self.disconnect()

    def disconnect(self):
        """ disconnect from IB host """
        if self.context is not None:
            self.disable_account_info_update()

        self.connection.eDisconnect()
        self.connected = False

    def register_strategy(self, context, data):
        """  TBA """
        self.context = context


    def __get_new_request_id(self):
        '''' genew request ID (ticker ID) in a thread safe way '''
        self.req_id_locker.acquire()
        self.tickerId += 1
        __id = self.tickerId
        self.req_id_locker.release()
        return __id

    #
    # Tick Data Methods
    #
    def request_tick_data(self, contract):
        """ Subscribe tick data for a specified contract
        Args:
            contract: a legal IBPY Contract object or a string for U.S. stock only
        Returns:
            tickerId:  the ID of this request. this ID could be used to cancel request later.
            tick_data: a reference to the tick data dictionary which will be updated with latest quote.
        """
        if isinstance(contract, Contract):
            pass
        elif isinstance(contract, str):
            contract = new_stock_contract(contract)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        __id = self.__get_new_request_id()
        request = RequestDetails('reqMktData', 'Snapshot', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        # False - indicating request live quotes instead of a snapshot
        self.connection.reqMktData(__id, contract, '', False)

        return __id, self.ipc_msg_dict[__id][1].tick_data

    def get_tick_snapshot(self, contract, max_wait_time=5):
        """ Get a snapshot with default tick types and corresponding tick data for a given contract

        Note: 1) no generic ticks can be specified.
              2) only return data fields which have changed within an 11 second interval.
              If it is necessary for an API client to receive a certain data field, it is better
              to subscribe to market data until that field has been returned and then cancel the market data request.

        Known Issues:
              1) When called outside of market hours, get_tick_snapshot request could take more than 10 sec
                 to reach the end (tickSnapshotEnd)
              2) Need to check Issue#1 during market hours

        Args:
            contract: a legal IBPY Contract object or a string for U.S. stock only

        Returns:
            a copy of tick data dictionary
        Raises:
            None
        """
        if isinstance(contract, Contract):
            pass
        elif isinstance(contract, str):
            contract = new_stock_contract(contract)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        __id = self.__get_new_request_id()

        request = RequestDetails('reqMktData', 'Snapshot', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        # send reqMktData req
        # True - indicating request live quotes instead of a snapshot
        #
        # Important:
        # When set it to 'True', each regulatory snapshot made will incur a fee of 0.01 USD to the account.
        # This applies to both live and paper accounts.
        self.connection.reqMktData(__id, contract, '', True)

        response.event.wait(max_wait_time)
        if response.event.is_set():
            # tickPrice() and tickeSize() may write after tickSnapshotEnd() completed.
            sleep(0.5)
            snapshot = copy(response.tick_data)
            # remove the from dict and free the memory
            response.event.clear()
            self.ipc_msg_dict.pop(__id)
        else:
            response.event.clear()
            self.ipc_msg_dict.pop(__id)
            raise RuntimeError('reqMktData (get_tick_snapshot) is timeout. max_wait_time=%d' % (max_wait_time))

        return snapshot

    def cancel_tick_request(self, tickerId):
        """ Cancel tick data request for a given ticker ID (request ID)

        Args:
            tickerId: the ticker request to cancel
        Returns:
            None
        Raises:
            None
        """
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        # TODO: check if tickerID is in the list
        self.connection.cancelMktData(tickerId)
        self.ipc_msg_dict.pop(tickerId)
        return

    def request_realtime_price(self, contract, price_type='TRADES'):
        """ Get real-time price/volume for a specific contract, e.g. stocks, futures and option contracts.
            IB API support only 5 sec duration between two real-time bar (price) records.
        Args:
            contract: one IB contract instance
            price_type: 'TRADES', 'MIDPOINT', 'BID',  'ASK'
        Returns:
            tickerId: the request ID; it's also the key to get response msg from ipc_msg_dict
            realtime_price: a reference to the real-time price (OCHL) list which will be updated
                            with latest price (OCHL) record.
        Raises:
            None
        """
        if isinstance(contract, Contract):
            pass
        elif isinstance(contract, str):
            contract = new_stock_contract(contract)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if price_type not in ['TRADES', 'MIDPOINT', 'BID', 'ASK']:
            raise TypeError("Got incorrect price_type")

        __id = self.__get_new_request_id()
        request = RequestDetails('reqHistoricalData', price_type, contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)
        # only 5 sec duration supported
        # price_type: 'TRADES', 'MIDPOINT', 'BID',  'ASK'
        # useRTH - set to True
        self.connection.reqRealTimeBars(__id, contract, 5, price_type, True)

        return __id, self.ipc_msg_dict[__id][1].rt_price

    def cancel_realtime_price(self, req_id):
        """ Cancel realtime price/volumne request.
        Args:
            req_id: the ticker ID (or request ID)
        Returns:
            None
        """
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')
        self.connection.cancelRealTimeBars(req_id)

        # remove request/response data from ipc_msg_dict
        self.ipc_msg_dict.pop(req_id)
        return

    #
    # Historical Data Methods
    #
    def get_price_history(self, contract, ts_end, duration='1 M', frequency='daily', max_wait_time=30):
        """ Get price/volumne history for a specific contract, e.g. stocks, futures and option ocntract.

        Args:
            contract: one IB contract instance
            ts_end: a string in '%Y%m%d' or '%Y%m%d %H:%M:%S' format
            duration: string
                        X S	Seconds
                        X D	Day
                        X W	Week
                        X M	Month
                        X Y	Year
            frequency: {‘daily’, ‘minute’}, optional; Resolution of the data to be returned.
            max_wait_time: int; max num of sec to wait after calling reqHistoricalData
        Returns:
            pandas Panel/DataFrame/Series – The pricing data that was requested.

                            Open  High   Low  Close     Volume
                Date
                2017-12-15  6.96  6.96  6.86   6.90  366523000
                2017-12-18  6.88  7.02  6.87   6.98  303664000
                2017-12-19  7.00  7.02  6.98   7.01  299342000

        Raises:
            None

        """
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(contract, Contract):
            pass
        elif isinstance(contract, str):
            contract = new_stock_contract(contract)
        else:
            raise TypeError("contract must be a Contract object or string")

        if frequency == 'daily':
            bar_size = '1 day'
        elif frequency == 'minute':
            bar_size = '1 min'
        elif frequency == 'second':
            bar_size = '1 sec'
        elif frequency == '5 seconds':
            bar_size = '5 secs'
        else:
            raise ValueError("get_price_history: incorrect frequency value")

        if len(ts_end) == 8 or len(ts_end) == 17:
            if len(ts_end) == 8:
                ts_end = ts_end + ' 23:59:59'
        else:
            print('get_price_history: incorrect ts_end format')
            return

        __id = self.__get_new_request_id()
        request = RequestDetails('reqHistoricalData', '', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        self.connection.reqHistoricalData(tickerId=__id, contract=contract, endDateTime=ts_end, durationStr=duration,
                                          barSizeSetting=bar_size, whatToShow='TRADES', useRTH=0, formatDate=1)

        df = None
        response.event.wait(max_wait_time)
        if response.event.is_set():
            df = pd.DataFrame(response.price_hist, columns=self.PRICE_DF_HEADER1)
            # clean up the time format
            date = df['time'][0]

            if len(date) == 8:
                df['time'] = pd.to_datetime(df['time'], format='%Y%m%d')
            elif len(date) == 18:
                # len('20161020 23:46:00') --> 2 Spaces!!!!!
                # adj_date = datetime.strptime(date, "%Y%m%d  %H:%M:%S")
                df['time'] = pd.to_datetime(df['time'], format="%Y%m%d  %H:%M:%S")
            else:
                # adj_date = datetime.strptime(date, "%Y%m%d %H:%M:%S")
                df['time'] = pd.to_datetime(df['time'], format="%Y%m%d %H:%M:%S")

            # TODO: check for timezone
            # exchange = request.contract.m_exchange
            # server_timezone = pytz.timezone("Asia/Shanghai")  # timezone where the server runs
            # mkt_timezone = pytz.timezone(IBEXCHANGE.get_timezone(exchange))  # Get Exchange's timezone
            # adj_date = server_timezone.localize(adj_date).astimezone(
            #     mkt_timezone)  # covert server time to Exchange's time
            # adj_date = adj_date.strftime("%Y%m%d %H:%M:%S")  # from datetime to string

            df = df.set_index('time')
            # remove the from dict and free the memory
            response.event.clear()
            self.ipc_msg_dict.pop(__id)
        else:
            self.ipc_msg_dict.pop(__id)
            print('reqHistoricalData is timeout.')
            raise RuntimeError('reqHistoricalData is timeout.')

        return df

    def get_stock_price_history(self, security_list, ts_end, duration='1 M', frequency='daily', max_wait_time=30):
        """Get price/volumne history for a list of stocks.

        Args:
            security_list: a list of security symbols, .e.g. ['IBM', 'DATA']
            endDateTime: a string in '%Y%m%d' or '%Y%m%d %H:%M:%S' format
            durationStr: see IB API doc.
            frequency: {‘daily’, ‘minute’}, optional; Resolution of the data to be returned.
            max_wait_time: int; max num of sec to wait after calling reqHistoricalData
        Returns:
            pandas Panel/DataFrame/Series – The pricing data that was requested.
        Raises:
            None

        """
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        num_secs = len(security_list)
        if num_secs <= 0:
            return

        if frequency == 'daily':
            bar_size = '1 day'
        elif frequency == 'minute':
            bar_size = '1 min'
        elif frequency == 'second':
            bar_size = '1 sec'
        elif frequency == '5 seconds':
            bar_size = '5 secs'
        else:
            print('get_stock_price_history: incorrect frequency')
            return

        if len(ts_end) == 8 or len(ts_end) == 17:
            if len(ts_end) == 8:
                ts_end = ts_end + ' 23:59:59'
        else:
            print('get_stock_price_history: incorrect ts_end format')
            return

        # ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(columns=self.PRICE_DF_HEADER2)
        for sec in security_list:

            __id = self.__get_new_request_id()

            contract = new_stock_contract(sec)
            request = RequestDetails('reqHistoricalData', '', contract)
            response = ResponseDetails()
            self.ipc_msg_dict[__id] = (request, response)

            self.connection.reqHistoricalData(tickerId=__id, contract=contract, endDateTime=ts_end,
                                              durationStr=duration, barSizeSetting=bar_size, whatToShow='TRADES',
                                              useRTH=0, formatDate=1)

            response.event.wait(max_wait_time)
            if response.event.is_set():

                df_tmp = pd.DataFrame(response.price_hist, columns=self.PRICE_DF_HEADER1)
                # clean up the time format
                date = df_tmp['time'][0]

                if len(date) == 8:
                    df_tmp['time'] = pd.to_datetime(df_tmp['time'], format='%Y%m%d')
                elif len(date) == 18:
                    # len('20161020 23:46:00') --> 2 Spaces!!!!!
                    # adj_date = datetime.strptime(date, "%Y%m%d  %H:%M:%S")
                    df_tmp['time'] = pd.to_datetime(df_tmp['time'], format="%Y%m%d  %H:%M:%S")
                else:
                    # adj_date = datetime.strptime(date, "%Y%m%d %H:%M:%S")
                    df_tmp['time'] = pd.to_datetime(df_tmp['time'], format="%Y%m%d %H:%M:%S")

                # TODO: check for timezone
                # exchange = request.contract.m_exchange
                # server_timezone = pytz.timezone("Asia/Shanghai")  # timezone where the server runs
                # mkt_timezone = pytz.timezone(IBEXCHANGE.get_timezone(exchange))  # Get Exchange's timezone
                # adj_date = server_timezone.localize(adj_date).astimezone(
                #     mkt_timezone)  # covert server time to Exchange's time
                # adj_date = adj_date.strftime("%Y%m%d %H:%M:%S")  # from datetime to string

                df_tmp['symbol'] = pd.DataFrame([sec] * len(df_tmp))
                df = df.append(df_tmp)
                # remove the from dict and free the memory
                self.ipc_msg_dict.pop(__id)
                response.event.clear()

            else:
                self.ipc_msg_dict.pop(__id)
                raise RuntimeError('reqHistoricalData is timeout.')

        return df

    def get_contract_price_history(self, contract, ts_end, duration='1 M', frequency='daily', max_wait_time=30):
        # Same function as get_price_history
        return self.get_price_history(contract, ts_end, duration, frequency, max_wait_time)

    #
    # Placing/Changing/Canceling Order Methods
    #
    def order_amount(self, contract, amount, style=MarketOrder()):
        ''' Place an order. Order X units of security Y.
            Warning: only mkt order and limited order work; calling stoploss/stoplimited order will result in IB disconnection.
        :param contract: A IB Contract object.
        :param amount: The integer amount of shares. Positive means buy, negative means sell.
        :param style:
        :return:
        '''
        if amount == 0:
            return -1
        elif amount > 0:
            action = 'BUY'
        else:
            action = 'SELL'

        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if not isinstance(contract, Contract):
            raise TypeError("contract must be a contract object")
        # request next valid order ID from IB host; this request will update self.order_id
        self.connection.reqIds(-1)  # note: input param is always ignored;
        sleep(0.05)

        order = Order()
        order.m_orderId = self.order_id
        order.m_client_id = self.client_id
        order.m_action = action
        order.m_totalQuantity = abs(amount)
        order.m_orderType = style.order_type
        if style.limit_price is not None:
            order.m_lmtPrice = style.limit_price
        if style.stop_price is not None:
            order.m_auxPrice = style.stop_price
        order.m_overridePercentageConstraints = True  # override TWS order size constraints

        # place order
        self.connection.placeOrder(self.order_id, contract, order)
        # TODO: wait for returns from orderStatus
        return self.order_id

    def combo_order_amount(self, contract, amount, style=MarketOrder()):
        ''' Place an order

        :param contract: A security object.
        :param amount: The integer amount of shares. Positive means buy, negative means sell.
        :param style:
        :return:
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if amount == 0:
            return -1
        elif amount > 0:
            action = 'BUY'
        else:
            action = 'SELL'

        if isinstance(contract, Contract):
            if len(contract.m_comboLegs) == 0:
                raise TypeError("contract must contains combo legs")
        else:
            raise TypeError("contract must be a contract object")

        # request next valid order ID from IB host; this request will update self.order_id
        self.connection.reqIds(-1)  # note: input param is always ignored;
        sleep(0.05)

        order = Order()
        order.m_orderId = self.order_id
        order.m_client_id = self.client_id
        order.m_action = action
        order.m_totalQuantity = abs(amount)
        order.m_orderType = style.order_type
        if style.limit_price is not None:
            order.m_lmtPrice = style.limit_price
        if style.stop_price is not None:
            order.m_auxPrice = style.stop_price

        order.m_overridePercentageConstraints = True  # override TWS order size constraints
        '''
        # Advanced configuration. Not tested yet.
        if style.is_combo_order:
            if style.non_guaranteed:
                tag = TagValue()
                tag.m_tag = "NonGuaranteed"
                tag.m_value = "1"
                order.m_smartComboRoutingParams = [tag]
        '''
        self.connection.placeOrder(self.order_id, contract, order)
        return self.order_id

    def order_value(self, contract, value, style):
        ''' Reserve for future implementation

        :param contract:
        :param value:
        :param style:
        :return:
        '''
        pass

    def order_target(self, contract, amount, style):
        ''' Places an order to adjust a position to a target number of shares.

        :param contract:
        :param value:
        :param style:
        :return:
        '''
        pass

    def order_target_value(self, contract, amount, style):
        ''' Places an order to adjust a position to a target value.

        :param contract:
        :param value:
        :param style:
        :return:
        '''
        pass

    def modify_order(self, order_id, contract, amount, style=MarketOrder()):
        ''' Change amount or order type (including limited price for limtied orders)
            for a existing order specified by order_id
        
        :param order_id: a existing order's order_id
        :param contract: A IB Contract object. supposed to be the same with the order-to-be-modified.
        :param amount: The integer amount of shares. Positive means buy, negative means sell.
        :param style: market order or limited order
        :return: the existing order's order_id (same as the input)
        '''

        if amount == 0:
            return -1
        elif amount > 0:
            action = 'BUY'
        else:
            action = 'SELL'

        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if not isinstance(contract, Contract):
            raise TypeError("contract must be a contract object")

        order = Order()
        order.m_orderId = order_id
        order.m_client_id = self.client_id
        order.m_action = action
        order.m_totalQuantity = abs(amount)
        order.m_orderType = style.order_type
        if style.limit_price is not None:
            order.m_lmtPrice = style.limit_price
        if style.stop_price is not None:
            order.m_auxPrice = style.stop_price
        order.m_overridePercentageConstraints = True  # override TWS order size constraints

        # place order
        self.connection.placeOrder(self.order_id, contract, order)
        # TODO: wait for returns from orderStatus
        return self.order_id

    def cancel_order(self, order):
        ''' Attempts to cancel the specified order. Cancel is attempted asynchronously.

        :param order: Can be the order_id as a string or the order object.
        :return: None
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(order, int):
            order_id = order
        elif isinstance(order, Order):
            order_id = order.m_orderId
        else:
            raise TypeError("order must be a order_id (int) or order object")
        self.connection.cancelOrder(order_id)

    def get_open_orders(self):
        ''' Attempts to get all open orders.

        :param
        :return: None
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if 'reqOpenOrders' not in self.ipc_msg_dict:
            request = RequestDetails('reqOpenOrders', '', '')
            response = ResponseDetails()
            self.ipc_msg_dict['reqOpenOrders'] = (request, response)
        else:
            response = self.ipc_msg_dict['reqOpenOrders'][1]

        # self.connection.reqOpenOrders()
        # self.reqAutoOpenOrders(True)
        self.connection.reqAllOpenOrders()

        max_wait_time = 3.
        self.get_order_event.wait(max_wait_time)
        if self.get_order_event.is_set():
            # snapshot = copy(response.tick_snapshot)
            # self.ipc_msg_dict.pop(self.tickerId)
            self.get_order_event.clear()
        else:
            # self.ipc_msg_dict.pop(self.tickerId)
            raise RuntimeError('get_open_orders is timeout.')

        return

    #
    # Account Info Methods
    #
    def enable_account_info_update(self):
        ''' Turn on auto account update, meaning IB socket host will push account info to IB socket client.
                updateAccountTime()
                updateAccountValue()
                updatePortfolio()
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        # TODO: check self.IB_acct_id before using it
        # request IB host (e.g. TWS) push account info to IB client (socket client)
        self.connection.reqAccountUpdates(True, self.context.account.account_id)
        return

    def disable_account_info_update(self):
        ''' Turn off auto account update, meaning IB socket host will stop pushing account info
         to IB socket client.
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        # TODO: check self.IB_acct_id before using it
        # stop IB host (e.g. TWS) to push account info to IB client (socket client)
        self.connection.reqAccountUpdates(False, self.context.account.account_id)
        return

    #
    # Fundamental Data Methods
    #
    def get_financial_statements(self, symbol, max_wait_time=20):
        ''' Get a company's financial statements

        :param:
            symbol: stock symbol string, e.g. 'IBM'; or a IB contract object
        :return:
            a string of financial statements
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(symbol, Contract):
            contract = symbol
        elif isinstance(symbol, str):
            contract = new_stock_contract(symbol)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        __id = self.__get_new_request_id()

        request = RequestDetails('reqFundamentalData', 'ReportsFinStatements', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        self.connection.reqFundamentalData(__id, contract, 'ReportsFinStatements')

        response.event.wait(max_wait_time)
        raw_xml = None
        if response.event.is_set():
            if response.status == ResponseDetails.STATUS_FINISHED:
                # covert from xml to dest. format
                raw_xml = copy(response.fundamental_data)
            else:
                pass  # raise RuntimeError('get_financial_statements: reqFundamentalData got error. Security=%s Reason:%s' % (symbol, response.error_msg))
        else:
            # Timeout
            pass  # ('get_financial_statements: reqFundamentalData is timeout. Security=%s' % symbol)

        status = response.status
        self.ipc_msg_dict.pop(__id)
        return status, raw_xml

    def get_company_ownership(self, symbol, max_wait_time=60.0 * 5):
        ''' Get a company's ownership report

        :param:
            symbol: stock symbol string, e.g. 'IBM'
            max_wait_time: max number of seconds to wait before raise timeout
        :return:
            a string of ownership report
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(symbol, Contract):
            contract = symbol
        elif isinstance(symbol, str):
            # For US stock only
            contract = new_stock_contract(symbol)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        __id = self.__get_new_request_id()

        request = RequestDetails('reqFundamentalData', 'ReportsOwnership', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        self.connection.reqFundamentalData(__id, contract, 'ReportsOwnership')

        response.event.wait(max_wait_time)
        report = None
        if response.event.is_set():
            if response.status == ResponseDetails.STATUS_FINISHED:
                # covert from xml to dest. format
                report = parse_ownership_report(response.fundamental_data)
            else:
                pass  # ('get_company_ownership: reqFundamentalData got error. Security=%s Reason:%s' % (symbol, response.error_msg))
        else:
            pass  # ('get_company_ownership: reqFundamentalData is timeout. Security=%s' % symbol)

        status = response.status
        self.ipc_msg_dict.pop(__id)
        return status, report

    def get_analyst_estimates(self, symbol, max_wait_time=20):
        ''' Get analyst estimates report for a company

        :param:
            symbol: stock symbol string, e.g. 'IBM'; or a IB contract object
        :return:
            a string of financial statements
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(symbol, Contract):
            contract = symbol
        elif isinstance(symbol, str):
            contract = new_stock_contract(symbol)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        __id = self.__get_new_request_id()

        request = RequestDetails('reqFundamentalData', 'RESC-Analyst Estimates', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        self.connection.reqFundamentalData(__id, contract, 'RESC')

        response.event.wait(max_wait_time)
        report = None
        if response.event.is_set():
            if response.status == ResponseDetails.STATUS_FINISHED:
                # covert from xml to dest. format
                report = parse_analyst_estimates(response.fundamental_data)
            else:
                pass  # ('get_analyst_estimates: reqFundamentalData got error. Security=%s Reason:%s' % (symbol, response.error_msg))
        else:
            pass  # ('get_analyst_estimates: reqFundamentalData is timeout. Security=%s' % symbol)

        status = response.status
        self.ipc_msg_dict.pop(__id)
        return status, report

    def get_company_overview(self, symbol, max_wait_time=10):
        ''' Get company overview infomration

        :param:
            symbol: stock symbol string, e.g. 'IBM'; or a IB contract object
        :return:
            a string of financial statements
        '''
        # ReportsFinSummary	Financial summary

        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(symbol, Contract):
            contract = symbol
        elif isinstance(symbol, str):
            contract = new_stock_contract(symbol)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        __id = self.__get_new_request_id()

        request = RequestDetails('reqFundamentalData', 'ReportSnapshot-Company overview', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        # ReportSnapshot	Company's financial overview
        self.connection.reqFundamentalData(__id, contract, 'ReportSnapshot')

        response.event.wait(max_wait_time)
        report = None
        if response.event.is_set():
            if response.status == ResponseDetails.STATUS_FINISHED:
                # TODO: covert from xml to dest. format
                report = response.fundamental_data
            else:
                pass  # ('get_analyst_estimates: reqFundamentalData got error. Security=%s Reason:%s' % (symbol, response.error_msg))
        else:
            pass  # ('get_analyst_estimates: reqFundamentalData is timeout. Security=%s' % symbol)

        status = response.status
        self.ipc_msg_dict.pop(__id)
        return status, report

    def get_financial_summary(self, symbol, max_wait_time=10):
        ''' Get company finanical summary information, such as revenue history, net profit, and dividends history.

        :param:
            symbol: stock symbol string, e.g. 'IBM'; or a IB contract object
        :return:
            a string of financial statements
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(symbol, Contract):
            contract = symbol
        elif isinstance(symbol, str):
            contract = new_stock_contract(symbol)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        __id = self.__get_new_request_id()

        request = RequestDetails('reqFundamentalData', 'ReportsFinSummary-Financial summary', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        self.connection.reqFundamentalData(__id, contract, 'ReportsFinSummary')

        response.event.wait(max_wait_time)
        report = None
        if response.event.is_set():
            if response.status == ResponseDetails.STATUS_FINISHED:
                # TODO: covert from xml to dest. format
                report = response.fundamental_data
            else:
                pass
        else:
            pass

        status = response.status
        self.ipc_msg_dict.pop(__id)
        return status, report

    def get_financial_ratios(self, symbol, max_wait_time=5):
        ''' Get analyst estimates report for a company

        :param:
            symbol: stock symbol string, e.g. 'IBM'
        :return:
            a string of financial statements
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(symbol, Contract):
            contract = symbol
        elif isinstance(symbol, str):
            contract = new_stock_contract(symbol)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        __id = self.__get_new_request_id()

        request = RequestDetails('reqFundamentalData', 'RESC-Analyst Estimates', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        # 258 - financial ratios
        '''
            TTMNPMGN=16.1298;NLOW=80.6;TTMPRCFPS=6.26675;TTMGROSMGN=60.76731;TTMCFSHR=15.004
            46;QCURRATIO=1.42071;TTMREV=259842;TTMINVTURN=5.28024;TTMOPMGN=14.22711;TTMPR2RE
            V=1.39703;AEPSNORM=8.55;TTMNIPEREM=144524.1;EPSCHNGYR=8.47727;TTMPRFCFPS=62.4260
            6;TTMRECTURN=19.99938;TTMPTMGN=17.88125;QCSHPS=40.50882;TTMFCF=5815;
            LATESTADATE=2016-12-31;APTMGNPCT=17.88125;AEBTNORM=46463;TTMNIAC=33008;NetDebt_I=152080;
            PRYTDPCTR=-1.55563;TTMEBITD=53326;AFEEPSNTM=0;PR2TANBK=5.01599;EPSTRENDGR=-
            15.53209;QTOTD2EQ=72.60778;TTMFCFSHR=1.50625;QBVPS=110.0867;NPRICE=94.1;YLD5YAVG
            =3.88751;REVTRENDGR=51.11774;TTMEPSXCLX=8.54981;QTANBVPS=18.75999;PRICE2BK=0.854
            78;MKTCAP=363007.5;TTMPAYRAT=31.32574;TTMINTCOV=-99999.99;TTMDIVSHR=2.585;TTMREVCHG=55.81794;
            TTMROAPCT=4.09615;TTMROEPCT=7.73685;
            TTMREVPERE=896006.9;APENORM=11.00585;TTMROIPCT=5.51924;REVCHNGYR=-
            6.66885;CURRENCY=HKD;DIVGRPCT=-8.33887;TTMEPSCHG=-32.80548;PEEXCLXOR=11.00609;QQUICKRATI=1.30087;
            TTMREVPS=67.30638;BETA=0.90979;TTMEBT=46463;ADIV5YAVG=3.1048;ANIACNORM=33008;QLTD2EQ=55.46377;NHIG=103.9
        '''
        report = None
        self.connection.reqMktData(__id, contract, "258", False)
        response.event.wait(max_wait_time)
        if response.event.is_set():
            if response.status == ResponseDetails.STATUS_FINISHED:
                # TODO: convert the format to a table alike
                report = response.tick_str

        return report

    def get_dividends_info(self, symbol, max_wait_time=5):
        ''' Get analyst estimates report for a company

        :param:
            symbol: stock symbol string, e.g. 'IBM'
        :return:
            a string of financial statements
        '''
        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        if isinstance(symbol, Contract):
            contract = symbol
        elif isinstance(symbol, str):
            contract = new_stock_contract(symbol)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        __id = self.__get_new_request_id()
        request = RequestDetails('reqFundamentalData', 'RESC-Analyst Estimates', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        # IB Dividends ("456")
        #
        # This tick type provides four different comma-separated elements:
        # The sum of dividends for the past 12 months (0.83 in the example below).
        # The sum of dividends for the next 12 months (0.92 from the example below).
        # The next dividend date (20130219 in the example below).
        # The next single dividend amount (0.23 from the example below).
        # Example: 0.83,0.92,20130219,0.23
        self.connection.reqMktData(__id, contract, "456", False)
        result = None
        response.event.wait(max_wait_time)
        if response.event.is_set():
            if response.status == ResponseDetails.STATUS_FINISHED:
                # TODO: convert the format
                result = set(response.tick_str.split(','))

        self.ipc_msg_dict.pop(__id)

        return result

    def get_contract_details(self, contract, max_wait_time=5):
        """ Get contract details for a specified contract
        Args:
            contract: a legal IBPY Contract object or a string for U.S. stock only
        Returns:
            status: a reference to the tick data dictionary which will be updated with latest quote.
            contract_details: a contractDetails instance
        """
        if isinstance(contract, Contract):
            pass
        elif isinstance(contract, str):
            contract = new_stock_contract(contract)
        else:
            raise TypeError("contract must be a contract object or string (for U.S. stocks only).")

        if not self.connected:
            raise RuntimeError('IB client is not connected to TWS')

        __id = self.__get_new_request_id()
        request = RequestDetails('reqContractDetails', '', contract)
        response = ResponseDetails()
        self.ipc_msg_dict[__id] = (request, response)

        # False - indicating request live quotes instead of a snapshot
        self.connection.reqContractDetails(__id, contract)

        response.event.wait(max_wait_time)
        contract_details = None
        if response.event.is_set():
            if response.status == ResponseDetails.STATUS_FINISHED:
                if len(response.contract_list) > 0:
                    contract_details = copy(response.contract_list[0])
            else:
                pass
        else:
            pass

        status = response.status
        self.ipc_msg_dict.pop(__id)

        return status, contract_details

    def get_full_contract(self, contract):
        """ Subscribe tick data for a specified contract
        Args:
            contract: a legal IBPY Contract object or a string for U.S. stock only
        Returns:
            tickerId:  the ID of this request. this ID could be used to cancel request later.
            tick_data: a reference to the tick data dictionary which will be updated with latest quote.
        """

        status, contract_details = self.get_contract_details(contract)
        new_contract = copy(contract_details.m_summary)

        return status, new_contract
