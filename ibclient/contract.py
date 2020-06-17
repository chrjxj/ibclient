# coding=utf-8

'''
Define factory functions to create IB contract instances
Created on 10/18/2016
@author: Jin Xu
@contact: jin_xu1@qq.com
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from ib.ext.Contract import Contract
from ib.ext.ComboLeg import ComboLeg


#
# Contract functions
#
def new_contract(contractTuple):
    ''' Create a new contract

    Args:
        contractTuple: contract's input in tuple
    Returns:
        a new contract object
    Raises:
        None
    '''
    contract = Contract()
    contract.m_symbol = contractTuple[0]
    contract.m_secType = contractTuple[1]
    contract.m_exchange = contractTuple[2]
    contract.m_currency = contractTuple[3]
    contract.m_expiry = contractTuple[4]
    contract.m_strike = contractTuple[5]
    contract.m_right = contractTuple[6]
    return contract


def new_stock_contract(symbol, exchange='SMART', primary_exchange=None, currency='USD', contract_id=None):
    ''' Create a new stock contract
    The function is implemented according to http://interactivebrokers.github.io/tws-api/basic_contracts.html
    Args:
        symbol: string of a stock symbol, e.g. 'IBM'
    Returns:
        a new stock contract object
    Raises:
        None
    '''
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = 'STK'
    contract.m_exchange = exchange
    # Specify the Primary Exchange attribute to avoid contract ambiguity
    if primary_exchange is None:
        contract.m_primaryExch = exchange
    else:
        contract.m_primaryExch = primary_exchange
    contract.m_localSymbol = symbol
    contract.m_currency = currency

    if contract_id is not None:
        contract.m_conId = contract_id

    return contract


def new_index_contract(symbol, currency='USD', exchange='SMART'):
    ''' Make an index contract.
    The function is implemented according to http://interactivebrokers.github.io/tws-api/basic_contracts.html
    Args:
        symbol: string of a stock symbol
    Returns:
        a new stock contract object
    Raises:
        None
    '''

    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = 'IND'
    contract.m_exchange = exchange
    contract.m_currency = currency
    return contract


def new_futures_contract(symbol, exchange, is_local_symbol, expiry=None, tradingClass=None, currency='USD',
                         is_expired=False, contract_id=0):
    ''' Make a new future contract
    The function is implemented according to http://interactivebrokers.github.io/tws-api/basic_contracts.html
    Args:
        symbol: string of a symbol or local symbol for the contract
        exchange: string of exchange name
        is_local_symbol: a True/False flag
        expiry: string; expiry month, e.g. '201610'
        tradingClass: string
    Returns:
        a new future contract object
    Raises:
        None
    '''

    if is_local_symbol is False:
        if expiry is None:
            print('new_futures_contract: get incorrect args.')
            return None

    contract = Contract()
    contract.m_secType = 'FUT'
    contract.m_exchange = exchange
    contract.m_currency = currency
    contract.m_conId = contract_id

    if is_local_symbol:
        contract.m_localSymbol = symbol  # e.g. 'VXV6', 'VXX6', 'VXZ6',
    else:
        contract.m_symbol = symbol
        contract.m_expiry = expiry

    if tradingClass is not None:
        contract.m_tradingClass = tradingClass

    if is_expired:
        contract.m_includeExpired = True

    return contract


# NOTE: tested
def new_future_spread_contract(symbol, id_to_buy, id_to_sell, exchange, currency='USD'):
    ''' Make a new future spread contract, e.g. calendar spread. The buy:sell ratio is 1 contract:1 contract
    The function is implemented according to http://interactivebrokers.github.io/tws-api/spread_contracts.html#bag_fut&gsc.tab=0

    :param symbol: symbol of a future contract; e.g. 'VIX'
    :param id_to_sell: a int number of contract ID (leg) to sell
    :param id_to_buy: a int number of contract ID (leg) to buy
    :param exchange: the exchange of contracts; string
    :param currency: the currency of the future contract
    :return: a new combo contract (future spread)
    '''

    contract = Contract()
    contract.m_symbol = symbol  # NOTE: do not set it to 'USD' for future spread as for option combo orders
    contract.m_secType = 'BAG'
    contract.m_currency = currency
    contract.m_exchange = 'SMART'  # set exchange to 'SMART' in the main order

    leg_to_sell = ComboLeg()
    leg_to_sell.m_conId = id_to_sell
    leg_to_sell.m_ratio = 1
    leg_to_sell.m_action = "SELL"
    leg_to_sell.m_exchange = exchange

    leg_to_buy = ComboLeg()
    leg_to_buy.m_conId = id_to_buy
    leg_to_buy.m_ratio = 1
    leg_to_buy.m_action = "BUY"
    leg_to_buy.m_exchange = exchange

    contract.m_comboLegs.append(leg_to_buy)
    contract.m_comboLegs.append(leg_to_sell)

    return contract


# NOTE: not tested
def new_stock_spread_contract(symbol, id_to_sell, id_to_buy, exchange='SMART', currency='USD'):
    ''' Make a new stock spread contract, e.g. a long/short pair. The buy:sell ratio is 1 contract:1 contract
    The function is implemented according to http://interactivebrokers.github.io/tws-api/spread_contracts.html#bag_fut&gsc.tab=0

    :param symbol: symbol of a stock contract; string
    :param id_to_sell: a int number of stock contract ID (leg) to sell
    :param id_to_buy: a int number of stock contract ID (leg) to buy
    :param exchange: the exchange of contracts; string
    :param currency: the currency of the future contract
    :return: a new combo contract (stock spread)
    '''
    contract = Contract()
    contract.m_symbol = symbol  # e.g. MCD stock
    contract.m_secType = 'BAG'
    contract.m_currency = currency
    contract.m_exchange = exchange

    leg_to_sell = ComboLeg()
    leg_to_sell.m_conId = id_to_sell  # e.g. MCD stock's contract ID
    leg_to_sell.m_ratio = 1
    leg_to_sell.m_action = "SELL"
    leg_to_sell.m_exchange = exchange
    leg_to_sell.m_openClose = 0

    leg_to_buy = ComboLeg()
    leg_to_buy.m_conId = id_to_buy  # e.g. IBKR stock's contract ID
    leg_to_buy.m_ratio = 1
    leg_to_buy.m_action = "BUY"
    leg_to_buy.m_exchange = exchange
    leg_to_buy.m_openClose = 0

    contract.m_comboLegs.append(leg_to_buy)
    contract.m_comboLegs.append(leg_to_sell)

    return contract


# NOTE: not tested
def new_option_contract(symbol, exchange, expiry=None, strike_price=None, trading_class=None, multiplier=100,
                        currency='USD', is_expired=False):
    ''' Make a new option contract. Options, like futures, also require an expiration date plus a strike and a multiplier.
    The function is implemented according to http://interactivebrokers.github.io/tws-api/basic_contracts.html
    Args:
        symbol: string of a symbol or local symbol for the contract
        exchange: string of exchange name
        is_local_symbol: a True/False flag
        expiry: string; expiry month, e.g. '201610'
        tradingClass: string
    Returns:
        a new future contract object
    Raises:
        None
    '''

    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = 'OPT'
    contract.m_exchange = exchange
    contract.m_expiry = expiry
    contract.m_strike = strike_price
    contract.m_right = "C"
    contract.m_multiplier = multiplier
    contract.m_currency = currency
    # It is not unusual to find many option contracts with an
    # almost identical description (i.e. underlying symbol, strike, last trading date, multiplier, etc.).
    # Adding more details such as the trading class will help:
    contract.m_tradingClass = trading_class

    if is_expired:
        contract.m_includeExpired = True

    return contract


# NOTE: not tested
def new_option_combo_contract(symbol, id_to_sell, id_to_buy, exchange='SMART', currency='USD'):
    ''' Make a new stock spread contract, e.g. a long/short pair. The buy:sell ratio is 1 contract:1 contract
    The function is implemented according to http://interactivebrokers.github.io/tws-api/spread_contracts.html#bag_fut&gsc.tab=0

    :param symbol: not used in this function.
    :param id_to_sell: a int number of stock contract ID (leg) to sell
    :param id_to_buy: a int number of stock contract ID (leg) to buy
    :param exchange: the exchange of contracts; string
    :param currency: the currency of the future contract
    :return: a new combo contract (stock spread)
    '''
    contract = Contract()
    contract.m_symbol = currency
    contract.m_secType = 'BAG'
    contract.m_currency = currency
    contract.m_exchange = 'SMART'

    leg_to_sell = ComboLeg()
    leg_to_sell.m_conId = id_to_sell  # e.g. MCD stock's contract ID
    leg_to_sell.m_ratio = 1
    leg_to_sell.m_action = "SELL"
    leg_to_sell.m_exchange = exchange
    leg_to_sell.m_openClose = 0

    leg_to_buy = ComboLeg()
    leg_to_buy.m_conId = id_to_buy  # e.g. IBKR stock's contract ID
    leg_to_buy.m_ratio = 1
    leg_to_buy.m_action = "BUY"
    leg_to_buy.m_exchange = exchange
    leg_to_buy.m_openClose = 0

    contract.m_comboLegs.append(leg_to_buy)
    contract.m_comboLegs.append(leg_to_sell)

    return contract


def convert_contract_to_dict(contract):
    '''
    A helping function that convert a contract instance to python dictionary
    :param contract: IB Contract instance
    :return: a dictionary
    '''
    contract_dict = {}
    contract_dict["conid"] = contract.m_conId
    contract_dict["symbol"] = contract.m_symbol
    contract_dict["secType"] = contract.m_secType
    contract_dict["expiry"] = contract.m_expiry
    contract_dict["strike"] = contract.m_strike
    contract_dict["right"] = contract.m_right
    contract_dict["multiplier"] = contract.m_multiplier
    contract_dict["exchange"] = contract.m_exchange
    contract_dict["primaryExch"] = contract.m_primaryExch
    contract_dict["currency"] = contract.m_currency
    contract_dict["localSymbol"] = contract.m_localSymbol
    contract_dict["tradingClass"] = contract.m_tradingClass

    return contract_dict


def convert_contract_details_to_dict(contractDetails):
    '''
    A helping function that convert a contract details instance to python dictionary
    :param contract: IB ContractDetails instance
    :return: a dictionary
    '''
    contract_details_dict = {}

    contract_details_dict["contract"] = contractDetails.m_summary

    contract_details_dict["marketName"] = contractDetails.m_marketName
    contract_details_dict["minTick"] = contractDetails.m_minTick
    contract_details_dict["price magnifier"] = contractDetails.m_priceMagnifier
    contract_details_dict["orderTypes"] = contractDetails.m_orderTypes
    contract_details_dict["validExchanges"] = contractDetails.m_validExchanges
    contract_details_dict["underConId"] = contractDetails.m_underConId
    contract_details_dict["longName"] = contractDetails.m_longName
    contract_details_dict["contractMonth"] = contractDetails.m_contractMonth
    contract_details_dict["industry"] = contractDetails.m_industry
    contract_details_dict["category"] = contractDetails.m_category
    contract_details_dict["subcategory"] = contractDetails.m_subcategory
    contract_details_dict["timeZoneId"] = contractDetails.m_timeZoneId
    contract_details_dict["tradingHours"] = contractDetails.m_tradingHours
    contract_details_dict["liquidHours"] = contractDetails.m_liquidHours
    contract_details_dict["evRule"] = contractDetails.m_evRule
    contract_details_dict["evMultiplier"] = contractDetails.m_evMultiplier

def convert_contract_sum_to_dict(contractDetails):
    '''
    A helping function that convert selected information in a contract details instance to python dictionary
    :param contract: IB ContractDetails instance
    :return: a dictionary
    '''

    contract_sum_dict = {}
    contract = contractDetails.m_summary

    contract_sum_dict["conid"] = contract.m_conId
    contract_sum_dict["symbol"] = contract.m_symbol
    contract_sum_dict["secType"] = contract.m_secType
    contract_sum_dict["expiry"] = contract.m_expiry
    contract_sum_dict["strike"] = contract.m_strike
    contract_sum_dict["right"] = contract.m_right
    contract_sum_dict["multiplier"] = contract.m_multiplier
    contract_sum_dict["exchange"] = contract.m_exchange
    contract_sum_dict["primaryExch"] = contract.m_primaryExch
    contract_sum_dict["currency"] = contract.m_currency
    contract_sum_dict["localSymbol"] = contract.m_localSymbol
    contract_sum_dict["tradingClass"] = contract.m_tradingClass

    contract_sum_dict["longName"] = contractDetails.m_longName
    contract_sum_dict["industry"] = contractDetails.m_industry
    contract_sum_dict["category"] = contractDetails.m_category
    contract_sum_dict["subcategory"] = contractDetails.m_subcategory

    return contract_sum_dict
