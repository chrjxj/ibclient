# coding=utf-8

'''
Define common used variables and functions
Created on 10/18/2016
@author: Jin Xu
@contact: jin_xu1@qq.com
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from threading import Event

class RequestDetails():
    def __init__(self, req_name, req_type=None, contract=None):
        self.func_name = req_name
        self.req_type = req_type
        self.contract = contract

class ResponseDetails():
    # Status Defition for this Response
    STATUS_FINISHED = 0

    def __init__(self):
        self.price_hist = []    # for historical price responses
        self.rt_price = []      # for real-time bar responses
        self.status = -1        # error_code in IBMsgWrapper
        self.request_id = -1
        self.error_msg = ''
        self.event = Event()
        self.fundamental_data = ''
        self.contract_list = []
        self.tick_str = None
        # tick_data stores either live tick data or a tick snapshot
        self.tick_data = {'bidVolume1'  :  -1,  'bidPrice1'    :  -1,
                          'askPrice1'    :  -1, 'askVolume1'   :  -1,
                          'lastPrice'    :  -1, 'lastVolume'   :  -1,
                          'highPrice'    :  -1, 'lowPrice'     :  -1,
                          'volume'       :  -1, 'preClosePrice':  -1,
                          'openPrice'   :  -1,  'openInterest':  -1,
                          'lastTradeTS': -1}

