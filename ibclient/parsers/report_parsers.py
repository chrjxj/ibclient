# coding=utf-8

'''
IB XML Message (mainly company fundamental related) Parser
Created on 10/18/2016
@author: Jin Xu
@contact: jin_xu1@qq.com
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import xml.etree.ElementTree as ET
import datetime
import pandas as pd


def parse_ownership_report(xml_str):
    ''' Covert ownership_report in XML format to a python dict
    :param xml_str: report in XML (msg from IB)
    :return: a dict instance with report in table-like format
    '''
    if xml_str is None or len(xml_str) == 0 or (not isinstance(xml_str, str)):
        return None

    xml_root = ET.fromstring(xml_str)

    report_dict = {}
    owner_list = []
    for child in xml_root:
        if child.tag == 'Owner':
            ower_id = child.attrib['ownerId']
            quant = owner_type = -1.
            owner_name = as_of_date = currency = 'unknown'
            for e in list(child):
                if e.tag == 'quantity':
                    quant = float(e.text)  # num of shares
                    as_of_date = e.attrib['asofDate']  # each element has a 'asOfDate'. Assume all of those are the same
                elif e.tag == 'type':
                    # type of owner: 1-insider 2-institutions or other companies 3-ETFs funds/Asset Mgmts/FAs
                    owner_type = int(e.text)
                elif e.tag == 'name':
                    owner_name = e.text
                else:
                    currency = e.text
            owner_list.append((ower_id, owner_name, owner_type, quant, currency, as_of_date))
        elif child.tag == 'ISIN':
            report_dict[child.tag] = child.text  # ISIN
        elif child.tag == 'floatShares':
            d = child.attrib  # reported date for num of float shares
            d[child.tag] = int(child.text)  # num of float shares
            report_dict[child.tag] = d

    report_dict['Owners'] = owner_list
    return report_dict


def parse_analyst_estimates(xml_str):
    ''' Covert analyst_estimates report in XML format to a dataframe

        Sample XML str this function take care of:
            <ConsValue dateType="CURR">948.6400</ConsValue>
            <ConsValue dateType="1WA">948.6400</ConsValue>
            <ConsValue dateType="1MA">919.7700</ConsValue>
            ......
            <ConsValue dateType="18MA">867.8370</ConsValue>

        Sample output
                        Mean  DnGradings  UpGradings   Median     High  NumOfEst       Low   StdDev
        Date
        2016-11-21  805.4552         NaN         NaN  812.694  948.640        40  418.6917  96.7278
        2016-11-14  805.4552           0           0  812.694  948.640        40  418.6917  96.7278
        2016-10-24  768.2915           2          17  784.017  919.770        40  418.6917  97.5963

    :param xml_str: report in XML (msg from IB)
    :return: a dataframe instance
    '''
    if xml_str is None or len(xml_str) == 0 or (not isinstance(xml_str, str)):
        return None

    xml_root = ET.fromstring(xml_str)
    # tree = ET.parse('AnlysisEst.xml') #('BABA.xml')
    # xml_root = tree.getroot()

    # prep date dict to parse dateType in XML to python date format
    date_type = {}
    today = datetime.date.today()
    curr_wk = today - datetime.timedelta(today.weekday())
    date_type['CURR'] = curr_wk
    date_type['1WA'] = curr_wk - datetime.timedelta(7)
    # from '1MA' -> '18MA'
    for i in range(1, 19):
        key = str(i) + 'MA'
        date_type[key] = curr_wk - datetime.timedelta(7 * 4 * i)

    # extract target price in XML to a dict
    report_dict = {}
    ticker = ''
    currency = ''
    for child in xml_root:
        if child.tag == 'Company':
            for e in list(child):
                if e.tag == 'CompanyInfo':
                    for e2 in list(e):
                        if e2.tag == 'Currency' and e2.attrib['type'] == 'CONSENSUS':
                            currency = e2.attrib['code']

                # <Company>
                #     <SecurityInfo>
                #         <Security code="1">
                #             <SecIds>
                #                 <SecId set="LOCAL" type="TICKER">IBM</SecId>
                if e.tag == 'SecurityInfo':
                    for e2 in list(e):
                        if e2.tag == 'Security':
                            for e3 in list(e2):
                                if e3.tag == 'SecIds':
                                    for e4 in list(e3):
                                        if e4.tag == 'SecId' and e4.attrib['type'] == 'TICKER':
                                            ticker = e4.text

        # TODO: add TS, e.g. current week, 1 week ago, 1 month ago and etc
        if child.tag == 'ConsEstimates':
            for e in list(child):
                if e.tag == 'NPEstimates':
                    for e2 in list(e):
                        # <NPEstimate type="TARGETPRICE" unit="U">
                        if e2.tag == 'NPEstimate' and e2.attrib['type'] == 'TARGETPRICE':
                            # <ConsEstimate type="High">
                            for e3 in list(e2):
                                key = e3.attrib['type']
                                report_dict[key] = []
                                # <ConsValue dateType="CURR">948.6400</ConsValue>
                                for e4 in list(e3):
                                    # CURR, 1WA, 1MA and etc
                                    date = date_type.get(e4.attrib['dateType'])
                                    # target price, std, num est. and etc
                                    num = float(e4.text)
                                    report_dict[key].append((date, num))

    if len(report_dict) == 0:
        return None

    # cover the dict to a pandas DataFrame
    key = 'Mean'
    assert (key in report_dict)
    target_price_df = pd.DataFrame(report_dict[key], columns=['Date', key]).set_index('Date')

    for key in report_dict:
        if key != 'Mean':
            target_price_df = target_price_df.join(
                pd.DataFrame(report_dict[key], columns=['Date', key]).set_index('Date'))

    target_price_df['Symbol'] = ticker
    target_price_df['Currency'] = currency

    return target_price_df


def parse_fin_statements(xml_str):
    ''' Covert fin_statements in XML format to a python dict
    :param xml_str: report in XML (msg from IB)
    :return: a dict instance with report in table-like format
    '''
    if xml_str is None or len(xml_str) == 0 or (not isinstance(xml_str, str)):
        return None

    xml_root = ET.fromstring(xml_str)
    report_dict = {}
    return report_dict


def parse_calendar_report(xml_str):
    ''' Covert ownership_report in XML format to a python dict
    :param xml_str: report in XML (msg from IB)
    :return: a dict instance with report in table-like format
    '''
    if xml_str is None or len(xml_str) == 0 or (not isinstance(xml_str, str)):
        return None

    xml_root = ET.fromstring(xml_str)
    report_dict = {}
    return report_dict
