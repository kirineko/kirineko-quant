from typing import List, Union, Optional

import os
from datetime import datetime

import pandas as pd
from pandas import Index
from jqdatasdk import *


auth('17620708831', 'As798360687')
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 20)

"""
- 获取所有A股股票列表
- 获取单个股票行情数据
- 导出股票行情数据
- 转换股票行情周期
- 获取单个股票财务指标
- 获取单个股票估值指标
"""


def get_stock_list() -> List[str]:
    """
    获取所有A股股票列表, 上海交易所: XSHG, 深圳交易所: XSHE
    :return:
    """
    stocks_list = list(get_all_securities(['stock']).index)
    return stocks_list


def get_single_price(code: str, time_freq: str,
                     start_date: Optional[Union[datetime, str]],
                     end_date: Union[datetime, str]) -> pd.DataFrame:
    # 如果start_data为None, 默认为上市日期开始
    if start_date is None:
        start_date = get_security_info(code).start_date
    data = get_price(code, start_date=start_date, end_date=end_date, frequency=time_freq)
    return data


def save_csv_data(data: pd.DataFrame, code, stock_type):
    dirname = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dirname, stock_type, code + '.csv')
    data.index.names = ['date']
    if os.path.isfile(path):
        data.to_csv(path, mode='a', header=False)
    else:
        data.to_csv(path)
    print('已成功存储至:', path)


def get_csv_data(code, stock_type) -> pd.DataFrame:
    dirname = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dirname, stock_type, code + '.csv')
    return pd.read_csv(path)


def transfer_price_freq(data: pd.DataFrame, time_freq) -> pd.DataFrame:
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()
    return df_trans


def get_single_finance(code, date, statDate) -> pd.DataFrame:
    data = get_fundamentals(query(indicator).filter(
        indicator.code == code
    ), date=date, statDate=statDate)
    return data


def get_single_valuation(code, date, statDate) -> pd.DataFrame:
    data = get_fundamentals(query(valuation).filter(
        valuation.code == code
    ), date=date, statDate=statDate)
    return data


def calculate_change_pct(data: pd.DataFrame) -> pd.DataFrame:
    """
    涨跌幅 = （当期收盘价 - 前期收盘价）/ 前期收盘价
    :param data: DataFrame,带有收盘价
    :return: DataFrame, 带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data
